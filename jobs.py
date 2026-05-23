from telegram.ext import ContextTypes
from services.provider_factory import get_provider
import models
from sqlalchemy.orm import Session
from common.lang_dicts import TEXTS, get_lang
from common.common import escape_html, format_float
import logging
from Config import Config

logger = logging.getLogger(__name__)


async def poll_api_orders_status(context: ContextTypes.DEFAULT_TYPE):
    """Poll API orders status and notify users when orders complete"""
    try:
        with models.session_scope() as s:
            non_terminal_orders = (
                s.query(models.ApiPurchaseOrder)
                .filter(
                    models.ApiPurchaseOrder.status.in_(
                        [
                            models.ApiPurchaseOrderStatus.PENDING,
                            models.ApiPurchaseOrderStatus.PROCESSING,
                        ]
                    )
                )
                .all()
            )

            if not non_terminal_orders:
                return

            logger.info(f"Polling {len(non_terminal_orders)} API orders...")

            for order in non_terminal_orders:
                try:
                    provider = get_provider(order.api_provider)
                    game_code = order.api_game_code
                    status_result = await provider.get_order_status(
                        str(order.api_order_id), game_code
                    )

                    new_status = status_result.status
                    api_message = status_result.message or ""
                    player_name = status_result.player_name
                    voucher_codes = status_result.voucher_codes

                    old_status = order.status
                    status_changed = old_status != new_status

                    with models.session_scope() as update_session:
                        db_order = update_session.get(
                            models.ApiPurchaseOrder, order.id
                        )
                        if db_order:
                            db_order.status = new_status
                            if api_message:
                                db_order.api_message = api_message
                            if player_name:
                                db_order.player_name = player_name
                            if voucher_codes:
                                db_order.set_voucher_codes(voucher_codes)

                            if status_changed and new_status in [
                                models.ApiPurchaseOrderStatus.FAILED,
                                models.ApiPurchaseOrderStatus.CANCELLED,
                            ]:
                                user = update_session.get(
                                    models.User, db_order.user_id
                                )
                                if user:
                                    user.balance += db_order.price_sudan
                                    logger.info(
                                        f"Refunded {db_order.price_sudan} SDG to user {user.user_id} "
                                        f"for failed/cancelled order {db_order.api_order_id}"
                                    )

                            update_session.commit()

                            if status_changed and db_order.is_terminal():
                                await notify_user_order_status(
                                    context, db_order, old_status, new_status, s
                                )

                except Exception as e:
                    logger.error(
                        f"Error polling order {order.api_order_id}: {str(e)}",
                        exc_info=True,
                    )
                    continue

    except Exception as e:
        logger.error(f"Error in poll_api_orders_status: {str(e)}", exc_info=True)


async def notify_user_order_status(
    context: ContextTypes.DEFAULT_TYPE,
    order: models.ApiPurchaseOrder,
    old_status,
    new_status,
    s: Session,
):
    """Notify user about order status change"""
    try:
        lang = get_lang(order.user_id)
        if new_status == models.ApiPurchaseOrderStatus.COMPLETED:
            status_emoji = "✅"
            status_text = TEXTS[lang].get(
                "api_order_completed",
                "Your order has been completed successfully!",
            )
        elif new_status == models.ApiPurchaseOrderStatus.FAILED:
            status_emoji = "❌"
            status_text = TEXTS[lang].get(
                "api_order_failed",
                "Your order has failed.",
            )
            refund_text = TEXTS[lang].get(
                "balance_refunded",
                "Your balance has been refunded: {amount} SDG",
            ).format(amount=format_float(order.price_sudan))
            status_text += f"\n\n💰 {refund_text}"
        elif new_status == models.ApiPurchaseOrderStatus.CANCELLED:
            status_emoji = "🚫"
            status_text = TEXTS[lang].get(
                "api_order_cancelled",
                "Your order has been cancelled.",
            )
            refund_text = TEXTS[lang].get(
                "balance_refunded",
                "Your balance has been refunded: {amount} SDG",
            ).format(amount=format_float(order.price_sudan))
            status_text += f"\n\n💰 {refund_text}"
        else:
            return

        message = f"{status_emoji} {status_text}\n\n"
        message += f"<b>{TEXTS[lang].get('order_id', 'Order ID')}:</b> <code>{order.api_order_id}</code>\n"
        game_name = "N/A"
        api_game = order.api_game
        if not api_game:
            api_game = s.query(models.ApiGame).filter(
                models.ApiGame.api_game_code == order.api_game_code,
                models.ApiGame.provider == order.api_provider,
            ).first()
        if api_game:
            game_name = (
                api_game.arabic_name
                if (lang == models.Language.ARABIC and api_game.arabic_name)
                else api_game.api_game_name
            )
        message += f"<b>{TEXTS[lang].get('game', 'Game')}:</b> {escape_html(game_name)}\n"
        message += f"<b>{TEXTS[lang].get('denomination', 'Denomination')}:</b> {escape_html(order.denomination_name)}\n"
        if order.player_id:
            message += f"<b>{TEXTS[lang].get('player_id', 'Player ID')}:</b> <code>{escape_html(order.player_id)}</code>\n"

        if order.player_name:
            message += f"<b>{TEXTS[lang].get('player_name', 'Player Name')}:</b> {escape_html(order.player_name)}\n"

        codes = order.get_voucher_codes()
        if codes:
            message += f"\n<b>{TEXTS[lang].get('voucher_codes', 'Voucher Codes')}:</b>\n"
            for code in codes:
                message += f"<code>{escape_html(code)}</code>\n"

        message += f"<b>{TEXTS[lang].get('price', 'Price')}:</b> <code>{format_float(order.price_sudan)} SDG</code>\n"

        await context.bot.send_message(
            chat_id=order.user_id,
            text=message,
        )
        user = s.get(models.User, order.user_id)
        await context.bot.send_message(
            chat_id=Config.API_PURCHASES_ARCHIVE_CHANNEL,
            text=(
                message
                + "\n\n"
                + f"<i>{TEXTS[lang].get('order_user_info', 'Order user info')}:</i>\n\n"
                + user.stringify(lang)
            ),
        )

        logger.info(
            f"Notified user {order.user_id} about order {order.api_order_id} "
            f"status change: {old_status.value} -> {new_status.value}"
        )

    except Exception as e:
        logger.error(
            f"Error notifying user {order.user_id} about order {order.id}: {str(e)}",
            exc_info=True,
        )
