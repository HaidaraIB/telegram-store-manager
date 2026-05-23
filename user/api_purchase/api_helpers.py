from typing import Optional, Tuple

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import models
from services.provider_factory import get_active_provider, get_active_provider_enum
from services.api_purchase_helpers import games_to_dict, denoms_to_catalogues
from services import provider_logging
from models.ApiProvider import ApiProvider


async def fetch_filtered_games() -> list:
    provider = get_active_provider()
    games = games_to_dict(await provider.list_games())
    from user.api_purchase.keyboards import filter_active_games

    return filter_active_games(games)


async def load_denominations(game_code: str) -> Optional[list]:
    """Return catalogue dict list or None if empty."""
    provider = get_active_provider()
    active_provider = get_active_provider_enum()
    log_name = active_provider.value
    denoms = await provider.get_denominations(game_code)
    if not denoms:
        return None
    if active_provider == ApiProvider.GAMEVOUCHERS:
        before = len(denoms)
        denoms = [d for d in denoms if d.stock > 0]
        provider_logging.log_api_call(
            log_name,
            "filter_in_stock",
            game_code=game_code,
            before=before,
            after=len(denoms),
        )
        if not denoms:
            return None
    return denoms_to_catalogues(denoms)


def get_api_game_display_name(game_code: str, default_name: str, lang) -> str:
    from user.api_purchase.keyboards import get_game_display_name

    return get_game_display_name(game_code, default_name, lang)


async def check_api_game_active(game_code: str) -> bool:
    active_provider = get_active_provider_enum()
    with models.session_scope() as s:
        return (
            s.query(models.ApiGame)
            .filter(
                models.ApiGame.api_game_code == game_code,
                models.ApiGame.is_active == True,
                models.ApiGame.provider == active_provider,
            )
            .first()
            is not None
        )


INSTANT_PURCHASE_CONFIRM = 4


def clear_instant_purchase_context(context: ContextTypes.DEFAULT_TYPE) -> None:
    for key in (
        "api_game_code",
        "api_game_name",
        "api_catalogues",
        "api_selected_denom",
        "api_player_id",
        "api_server_id",
        "api_requires_server",
        "api_servers",
        "api_requires_player_id",
        "api_player_name",
    ):
        context.user_data.pop(key, None)


async def show_order_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Final review step — no API call and no balance deduction until user confirms."""
    from common.lang_dicts import TEXTS, get_lang
    from common.common import escape_html, format_float, get_exchange_rate
    from user.api_purchase.keyboards import build_order_confirm_keyboard

    lang = get_lang(update.effective_user.id)
    selected_denom = context.user_data.get("api_selected_denom", {})
    game_name = context.user_data.get("api_game_name", "")
    player_id = context.user_data.get("api_player_id")
    server_id = context.user_data.get("api_server_id")

    exchange_rate = get_exchange_rate()
    price_sudan = float(selected_denom.get("amount", 0)) * exchange_rate

    with models.session_scope() as session:
        user = session.get(models.User, update.effective_user.id)
        balance = float(user.balance) if user else 0.0

    player_line = ""
    if player_id:
        player_line = TEXTS[lang].get(
            "order_confirm_player_line",
            "🆔 <b>Player ID:</b> <code>{player_id}</code>\n",
        ).format(player_id=escape_html(player_id))
    server_line = ""
    if server_id:
        server_line = TEXTS[lang].get(
            "order_confirm_server_line",
            "🌐 <b>Server:</b> <code>{server_id}</code>\n",
        ).format(server_id=escape_html(server_id))

    text = (
        TEXTS[lang]
        .get("order_confirm_summary", "Confirm your order")
        .format(
            game_name=escape_html(game_name),
            denomination=escape_html(selected_denom.get("name", "")),
            price=format_float(price_sudan),
            player_line=player_line,
            server_line=server_line,
            balance=format_float(balance),
        )
    )

    back_cb = (
        "back_to_api_player_id"
        if context.user_data.get("api_requires_player_id")
        else "back_to_api_denom"
    )
    keyboard = build_order_confirm_keyboard(lang, back_callback=back_cb)

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=keyboard,
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    return INSTANT_PURCHASE_CONFIRM


async def proceed_after_denomination(
    selected_denom: dict,
    game_code: str,
    context,
    lang,
    update,
) -> Tuple[str, bool]:
    """
    Returns (next_step, skip_player).
    next_step: 'denomination' | 'player_id' | 'confirm'
    skip_player True means show confirmation (voucher — no player ID step).
    """
    from user.api_purchase.keyboards import build_player_id_keyboard
    from common.common import format_float, get_exchange_rate
    from common.lang_dicts import TEXTS
    from common.common import escape_html

    provider = get_active_provider()
    active_provider = get_active_provider_enum()
    denom_price_usd = float(selected_denom.get("amount", 0))
    exchange_rate = get_exchange_rate()
    denom_price_sudan = denom_price_usd * exchange_rate
    provider_logging.log_price_conversion(
        active_provider.value,
        "denom_selected",
        selected_denom.get("name", ""),
        denom_price_usd,
        selected_denom.get("currency", "USD"),
        user_id=update.effective_user.id,
        product_id=str(selected_denom.get("id", "")),
    )

    with models.session_scope() as session:
        user = session.get(models.User, update.effective_user.id)
        user_balance_sudan = float(user.balance) if user else 0.0

    if user_balance_sudan < denom_price_sudan:
        await update.callback_query.answer(
            text=TEXTS[lang]
            .get(
                "insufficient_balance_charge",
                "Insufficient balance ❌\nYour current balance: {balance} SDG\nRequired price: {price} SDG\n\nPlease charge your balance first 💰",
            )
            .format(
                balance=format_float(user_balance_sudan),
                price=format_float(denom_price_sudan),
            ),
            show_alert=True,
        )
        return "denomination", False

    balance_info = await provider.get_balance()
    provider_logging.log_api_call(
        active_provider.value,
        "stock_check",
        product_usd=denom_price_usd,
        wallet_available=balance_info.available_usd,
        wallet_currency=balance_info.currency,
    )
    if balance_info.available_usd < denom_price_usd:
        await update.callback_query.answer(
            text=TEXTS[lang].get(
                "product_out_of_stock",
                "This product is currently out of stock ❌\nWe apologize for the inconvenience",
            ),
            show_alert=True,
        )
        return "denomination", False

    requires_player = selected_denom.get("requires_player_id", True)
    servers = await provider.get_servers(game_code)
    context.user_data["api_requires_server"] = (
        servers is not None and len(servers or {}) > 0
    )
    context.user_data["api_servers"] = servers or {}
    context.user_data["api_requires_player_id"] = requires_player

    game_name = context.user_data.get("api_game_name", game_code)
    denom_name = selected_denom.get("name", "")

    if not requires_player:
        return "confirm", True

    enter_player = TEXTS[lang].get("enter_player_id", "Enter Player ID:")
    product_details_text = (
        TEXTS[lang]
        .get(
            "product_details_text",
            "<b>Product Details:</b>\n\n"
            "🎮 <b>Game:</b> {game_name}\n"
            "📦 <b>Denomination:</b> {denomination}\n"
            "💰 <b>Price:</b> {price}\n\n"
            "{enter_player_id}",
        )
        .format(
            game_name=escape_html(game_name),
            denomination=escape_html(denom_name),
            price=f"{format_float(denom_price_sudan)} SDG",
            enter_player_id=enter_player,
        )
    )

    await update.callback_query.edit_message_text(
        text=product_details_text,
        reply_markup=build_player_id_keyboard(lang),
    )
    return "player_id", False
