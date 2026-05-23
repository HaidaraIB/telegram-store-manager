from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from common.keyboards import build_user_keyboard
from common.lang_dicts import TEXTS, get_lang
from common.back_to_home_page import back_to_user_home_page_handler
from common.common import escape_html, format_float, get_exchange_rate
from common.decorators import is_user_banned
from custom_filters import PrivateChat
from start import start_command, admin_command
import uuid
from services.provider_factory import get_active_provider, get_active_provider_enum
from services import provider_logging
from services.api_purchase_helpers import catalogue_to_denomination
from user.api_purchase.api_helpers import (
    fetch_filtered_games,
    load_denominations,
    get_api_game_display_name,
    check_api_game_active,
    proceed_after_denomination,
    show_order_confirmation,
    clear_instant_purchase_context,
    INSTANT_PURCHASE_CONFIRM,
)
from user.api_purchase.keyboards import (
    build_game_keyboard,
    build_denomination_keyboard,
    build_server_keyboard,
    build_player_id_keyboard,
    build_search_results_keyboard,
    filter_active_games,
)
import models

# Conversation states for instant purchase
(
    INSTANT_PURCHASE_GAME,
    INSTANT_PURCHASE_DENOMINATION,
    INSTANT_PURCHASE_PLAYER_ID,
    INSTANT_PURCHASE_SERVER_ID,
) = range(4)
# INSTANT_PURCHASE_CONFIRM is defined in api_helpers (value 4)


@is_user_banned
async def instant_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for instant purchase flow"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        try:
            games = await fetch_filtered_games()

            if not games:
                await update.callback_query.answer(
                    text=TEXTS[lang].get("no_games_available", "No games available"),
                    show_alert=True,
                )
                return ConversationHandler.END

            # Store filtered games in context for pagination
            context.user_data["api_all_games"] = games
            context.user_data["api_games_page"] = 0

            search_hint = TEXTS[lang].get(
                "search_game_hint",
                "\n\n💡 يمكنك أيضاً كتابة اسم اللعبة للبحث عنها\n💡 You can also type the game name to search",
            )

            await update.callback_query.edit_message_text(
                text=TEXTS[lang].get(
                    "select_game_api", "Select game for instant purchase:"
                )
                + search_hint,
                reply_markup=build_game_keyboard(games, lang, page=0),
            )
            return INSTANT_PURCHASE_GAME
        except Exception as e:
            await update.callback_query.answer(
                text=TEXTS[lang].get("api_error", "Error connecting to service"),
                show_alert=True,
            )
            return ConversationHandler.END


@is_user_banned
async def get_instant_purchase_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle game selection and show denominations, or pagination"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)

        # Handle search results pagination
        if update.callback_query.data.startswith("api_search_page_"):
            page_str = update.callback_query.data.replace("api_search_page_", "")
            if page_str == "info":
                await update.callback_query.answer()
                return INSTANT_PURCHASE_GAME

            try:
                page = int(page_str)
                search_results = context.user_data.get("api_search_results", [])

                if not search_results:
                    await update.callback_query.answer(
                        text=TEXTS[lang].get(
                            "api_error", "Error connecting to service"
                        ),
                        show_alert=True,
                    )
                    return INSTANT_PURCHASE_GAME

                from user.api_purchase.keyboards import SEARCH_RESULTS_PER_PAGE

                total_pages = (
                    len(search_results) + SEARCH_RESULTS_PER_PAGE - 1
                ) // SEARCH_RESULTS_PER_PAGE
                page = max(0, min(page, total_pages - 1))
                context.user_data["api_search_page"] = page

                results_count = len(search_results)
                if lang == models.Language.ARABIC:
                    results_text = f"🔍 تم العثور على {results_count} نتائج:\nاختر اللعبة من القائمة:"
                else:
                    results_text = f"🔍 Found {results_count} results:\nSelect a game from the list:"

                await update.callback_query.edit_message_text(
                    text=results_text,
                    reply_markup=build_search_results_keyboard(
                        search_results, lang, page=page
                    ),
                )
                return INSTANT_PURCHASE_GAME
            except (ValueError, IndexError):
                await update.callback_query.answer(
                    text=TEXTS[lang].get("api_error", "Error connecting to service"),
                    show_alert=True,
                )
                return INSTANT_PURCHASE_GAME

        # Handle games pagination
        if update.callback_query.data.startswith("api_games_page_"):
            page_str = update.callback_query.data.replace("api_games_page_", "")
            if page_str == "info":
                # Just show current page info, don't change page
                await update.callback_query.answer()
                return INSTANT_PURCHASE_GAME

            try:
                page = int(page_str)
                games = context.user_data.get("api_all_games", [])

                if not games:
                    games = await fetch_filtered_games()
                    context.user_data["api_all_games"] = games

                total_pages = (len(games) + 6 - 1) // 6  # GAMES_PER_PAGE = 6
                page = max(0, min(page, total_pages - 1))  # Clamp page number
                context.user_data["api_games_page"] = page

                search_hint = TEXTS[lang].get(
                    "search_game_hint",
                    "\n\n💡 يمكنك أيضاً كتابة اسم اللعبة للبحث عنها\n💡 You can also type the game name to search",
                )

                await update.callback_query.edit_message_text(
                    text=TEXTS[lang].get(
                        "select_game_api", "Select game for instant purchase:"
                    )
                    + search_hint,
                    reply_markup=build_game_keyboard(games, lang, page=page),
                )
                return INSTANT_PURCHASE_GAME
            except (ValueError, IndexError):
                await update.callback_query.answer(
                    text=TEXTS[lang].get("api_error", "Error connecting to service"),
                    show_alert=True,
                )
                return INSTANT_PURCHASE_GAME

        # Handle game selection
        if not update.callback_query.data.startswith("back"):
            game_code = update.callback_query.data.replace("api_game_", "")
            # Validate that the game is an active filtered game
            if not await check_api_game_active(game_code):
                await update.callback_query.answer(
                    text=TEXTS[lang].get(
                        "game_not_available", "This game is not available"
                    ),
                    show_alert=True,
                )
                return INSTANT_PURCHASE_GAME
            context.user_data["api_game_code"] = game_code
        else:
            game_code = context.user_data.get("api_game_code")

        if not game_code:
            return INSTANT_PURCHASE_GAME

        try:
            catalogues = await load_denominations(game_code)

            if not catalogues:
                await update.callback_query.answer(
                    text=TEXTS[lang].get(
                        "no_denominations_available", "No denominations available"
                    ),
                    show_alert=True,
                )
                return INSTANT_PURCHASE_GAME

            lang = get_lang(update.effective_user.id)
            games = context.user_data.get("api_all_games", [])
            default_name = game_code
            for g in games:
                if g.get("code") == game_code:
                    default_name = g.get("name", game_code)
                    break
            display_name = get_api_game_display_name(game_code, default_name, lang)

            context.user_data["api_game_name"] = display_name
            context.user_data["api_catalogues"] = catalogues
            context.user_data["api_denoms_page"] = 0

            await update.callback_query.edit_message_text(
                text=TEXTS[lang].get("select_denomination", "Select denomination:"),
                reply_markup=build_denomination_keyboard(catalogues, lang, page=0),
            )
            return INSTANT_PURCHASE_DENOMINATION
        except Exception as e:
            await update.callback_query.answer(
                text=TEXTS[lang].get("api_error", "Error connecting to service"),
                show_alert=True,
            )
            return INSTANT_PURCHASE_GAME


def search_games(games: list, query: str, lang: models.Language = None) -> list:
    """Search games by name (case-insensitive, partial match)
    Searches in original name, code, and Arabic name if available"""
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    # Get all active filtered games with their Arabic names for search
    api_games_dict = {}
    if lang:
        active_provider = get_active_provider_enum()
        with models.session_scope() as s:
            api_games_dict = {
                game.api_game_code: game
                for game in s.query(models.ApiGame)
                .filter(
                    models.ApiGame.is_active == True,
                    models.ApiGame.provider == active_provider,
                )
                .all()
            }

    results = []
    for game in games:
        game_name = game.get("name", "").lower()
        game_code = game.get("code", "").lower()

        # Check if query matches original game name or code
        matches = query_lower in game_name or query_lower in game_code

        # Also check Arabic name if available
        if not matches and lang and game_code in api_games_dict:
            api_game = api_games_dict[game_code]
            if api_game.arabic_name:
                arabic_name_lower = api_game.arabic_name.lower()
                if query_lower in arabic_name_lower:
                    matches = True

        if matches:
            results.append(game)

    return results


@is_user_banned
async def handle_game_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text message for game search"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        search_query = update.message.text.strip()

        # Get games from context or reload
        games = context.user_data.get("api_all_games", [])
        if not games:
            try:
                games = await fetch_filtered_games()
                context.user_data["api_all_games"] = games
            except Exception:
                await update.message.reply_text(
                    text=TEXTS[lang].get("api_error", "Error connecting to service"),
                )
                return INSTANT_PURCHASE_GAME

        # Search for games (already filtered)
        search_results = search_games(games, search_query, lang)

        if not search_results:
            # No results found
            if lang == models.Language.ARABIC:
                no_results_text = f"❌ لم يتم العثور على نتائج للبحث: '{search_query}'\n\n💡 جرب البحث مرة أخرى أو اختر من القائمة"
            else:
                no_results_text = f"❌ No results found for: '{search_query}'\n\n💡 Try searching again or select from the list"

            await update.message.reply_text(
                text=no_results_text,
            )
            return INSTANT_PURCHASE_GAME

        if len(search_results) == 1:
            # Single result - proceed directly
            game = search_results[0]
            game_code = game.get("code")

            if not await check_api_game_active(game_code):
                await update.message.reply_text(
                    text=TEXTS[lang].get(
                        "game_not_available", "This game is not available"
                    ),
                )
                return INSTANT_PURCHASE_GAME

            context.user_data["api_game_code"] = game_code

            try:
                catalogues = await load_denominations(game_code)

                if not catalogues:
                    await update.message.reply_text(
                        text=TEXTS[lang].get(
                            "no_denominations_available", "No denominations available"
                        ),
                    )
                    return INSTANT_PURCHASE_GAME

                context.user_data["api_game_name"] = get_api_game_display_name(
                    game_code, game.get("name", game_code), lang
                )
                context.user_data["api_catalogues"] = catalogues
                context.user_data["api_denoms_page"] = 0

                await update.message.reply_text(
                    text=TEXTS[lang].get("select_denomination", "Select denomination:"),
                    reply_markup=build_denomination_keyboard(catalogues, lang, page=0),
                )
                return INSTANT_PURCHASE_DENOMINATION
            except Exception as e:
                await update.message.reply_text(
                    text=TEXTS[lang].get("api_error", "Error connecting to service"),
                )
                return INSTANT_PURCHASE_GAME
        else:
            # Multiple results - show keyboard with pagination
            results_count = len(search_results)
            context.user_data["api_search_results"] = search_results
            context.user_data["api_search_page"] = 0

            if lang == models.Language.ARABIC:
                results_text = (
                    f"🔍 تم العثور على {results_count} نتائج:\nاختر اللعبة من القائمة:"
                )
            else:
                results_text = (
                    f"🔍 Found {results_count} results:\nSelect a game from the list:"
                )

            await update.message.reply_text(
                text=results_text,
                reply_markup=build_search_results_keyboard(
                    search_results, lang, page=0
                ),
            )
            return INSTANT_PURCHASE_GAME


@is_user_banned
async def back_to_api_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back to games list (first page)"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        games = context.user_data.get("api_all_games", [])

        if not games:
            try:
                games = await fetch_filtered_games()
                context.user_data["api_all_games"] = games
            except Exception:
                return await instant_purchase(update, context)

        context.user_data["api_games_page"] = 0

        search_hint = TEXTS[lang].get(
            "search_game_hint",
            "\n\n💡 يمكنك أيضاً كتابة اسم اللعبة للبحث عنها\n💡 You can also type the game name to search",
        )

        await update.callback_query.edit_message_text(
            text=TEXTS[lang].get("select_game_api", "Select game for instant purchase:")
            + search_hint,
            reply_markup=build_game_keyboard(games, lang, page=0),
        )
        return INSTANT_PURCHASE_GAME


@is_user_banned
async def get_instant_purchase_denomination(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle denomination selection and get required fields, or pagination"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)

        # Handle pagination
        if update.callback_query.data.startswith("api_denoms_page_"):
            page_str = update.callback_query.data.replace("api_denoms_page_", "")
            if page_str == "info":
                # Just show current page info, don't change page
                await update.callback_query.answer()
                return INSTANT_PURCHASE_DENOMINATION

            try:
                page = int(page_str)
                catalogues = context.user_data.get("api_catalogues", [])

                if not catalogues:
                    await update.callback_query.answer(
                        text=TEXTS[lang].get(
                            "api_error", "Error connecting to service"
                        ),
                        show_alert=True,
                    )
                    return INSTANT_PURCHASE_DENOMINATION

                from user.api_purchase.keyboards import DENOMINATIONS_PER_PAGE

                total_pages = (
                    len(catalogues) + DENOMINATIONS_PER_PAGE - 1
                ) // DENOMINATIONS_PER_PAGE
                page = max(0, min(page, total_pages - 1))  # Clamp page number
                context.user_data["api_denoms_page"] = page

                await update.callback_query.edit_message_text(
                    text=TEXTS[lang].get("select_denomination", "Select denomination:"),
                    reply_markup=build_denomination_keyboard(
                        catalogues, lang, page=page
                    ),
                )
                return INSTANT_PURCHASE_DENOMINATION
            except (ValueError, IndexError):
                await update.callback_query.answer(
                    text=TEXTS[lang].get("api_error", "Error connecting to service"),
                    show_alert=True,
                )
                return INSTANT_PURCHASE_DENOMINATION

        # Handle denomination selection
        if not update.callback_query.data.startswith("back"):
            denom_index = int(update.callback_query.data.replace("api_denom_", ""))
            catalogues = context.user_data.get("api_catalogues", [])

            if denom_index >= len(catalogues):
                await update.callback_query.answer(
                    text=TEXTS[lang].get("api_error", "Error connecting to service"),
                    show_alert=True,
                )
                return INSTANT_PURCHASE_DENOMINATION

            selected_denom = catalogues[denom_index]
            context.user_data["api_selected_denom"] = selected_denom
        else:
            selected_denom = context.user_data.get("api_selected_denom")

        if not selected_denom:
            return INSTANT_PURCHASE_DENOMINATION

        try:
            game_code = context.user_data.get("api_game_code")
            next_step, skip_player = await proceed_after_denomination(
                selected_denom, game_code, context, lang, update
            )
            if next_step == "denomination":
                return INSTANT_PURCHASE_DENOMINATION
            if skip_player:
                context.user_data["api_player_id"] = None
                return await show_order_confirmation(update, context)
            return INSTANT_PURCHASE_PLAYER_ID
        except Exception as e:
            await update.callback_query.answer(
                text=TEXTS[lang].get("api_error", "Error connecting to service"),
                show_alert=True,
            )
            return INSTANT_PURCHASE_DENOMINATION


back_to_api_denom = get_instant_purchase_game


@is_user_banned
async def get_instant_purchase_player_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle player ID input and validate it"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)

        player_id = update.message.text.strip()
        context.user_data["api_player_id"] = player_id

        try:
            provider = get_active_provider()
            game_code = context.user_data.get("api_game_code")
            requires_server = context.user_data.get("api_requires_server", False)

            validation_msg = await update.message.reply_text(
                text=TEXTS[lang].get("validating_player_id", "Validating player ID..."),
            )

            if requires_server:
                servers = context.user_data.get("api_servers", {})
                if servers:
                    await validation_msg.delete()
                    await update.message.reply_text(
                        text=TEXTS[lang].get("enter_server_id", "Enter Server ID:"),
                        reply_markup=build_server_keyboard(servers, lang),
                    )
                    return INSTANT_PURCHASE_SERVER_ID
                await validation_msg.delete()
                return await show_order_confirmation(update, context)

            check_result = await provider.validate_player_id(game_code, player_id)
            if check_result.valid:
                if check_result.player_name:
                    context.user_data["api_player_name"] = check_result.player_name
                    await validation_msg.edit_text(
                        text=TEXTS[lang]
                        .get(
                            "player_id_valid",
                            "Player ID validated ✅\nName: {player_name}",
                        )
                        .format(player_name=escape_html(check_result.player_name)),
                    )
                else:
                    await validation_msg.delete()
                return await show_order_confirmation(update, context)

            await validation_msg.edit_text(
                text=TEXTS[lang].get("player_id_invalid", "Invalid player ID ❌"),
            )
            return INSTANT_PURCHASE_PLAYER_ID
        except Exception as e:
            await update.message.reply_text(
                text=TEXTS[lang].get("api_error", "Error connecting to service"),
            )
            return INSTANT_PURCHASE_PLAYER_ID


back_to_api_player_id = get_instant_purchase_denomination


@is_user_banned
async def get_instant_purchase_confirm(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Confirm places the order; cancel exits without charging."""
    if not PrivateChat().filter(update):
        return ConversationHandler.END

    lang = get_lang(update.effective_user.id)
    data = update.callback_query.data

    if data == "api_cancel_order":
        await update.callback_query.answer()
        clear_instant_purchase_context(context)
        await update.callback_query.edit_message_text(
            text=TEXTS[lang].get(
                "api_purchase_cancelled_no_charge",
                "Order cancelled. No balance was deducted ✅",
            ),
            reply_markup=build_user_keyboard(lang),
        )
        return ConversationHandler.END

    if data == "api_confirm_order":
        await update.callback_query.answer()
        return await create_api_order(update, context)

    return INSTANT_PURCHASE_CONFIRM


@is_user_banned
async def get_instant_purchase_server_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Handle server ID selection and validate player ID"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)

        if update.callback_query.data.startswith("back"):
            # Go back to player ID input
            await update.callback_query.edit_message_text(
                text=TEXTS[lang].get("enter_player_id", "Enter Player ID:"),
                reply_markup=build_player_id_keyboard(lang),
            )
            return INSTANT_PURCHASE_PLAYER_ID

        # Get selected server
        server_key = update.callback_query.data.replace("api_server_", "")
        servers = context.user_data.get("api_servers", {})
        server_id = servers.get(server_key)
        context.user_data["api_server_id"] = server_id

        try:
            provider = get_active_provider()
            game_code = context.user_data.get("api_game_code")
            player_id = context.user_data.get("api_player_id")

            validation_msg = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=TEXTS[lang].get("validating_player_id", "Validating player ID..."),
            )

            check_result = await provider.validate_player_id(
                game_code, player_id, server_id
            )
            if check_result.valid:
                if check_result.player_name:
                    context.user_data["api_player_name"] = check_result.player_name
                    await validation_msg.edit_text(
                        text=TEXTS[lang]
                        .get(
                            "player_id_valid",
                            "Player ID validated ✅\nName: {player_name}",
                        )
                        .format(player_name=escape_html(check_result.player_name)),
                    )
                else:
                    await validation_msg.delete()
                return await show_order_confirmation(update, context)

            await validation_msg.edit_text(
                text=TEXTS[lang].get("player_id_invalid", "Invalid player ID ❌"),
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=TEXTS[lang].get("enter_player_id", "Enter Player ID:"),
                reply_markup=build_player_id_keyboard(lang),
            )
            return INSTANT_PURCHASE_PLAYER_ID
        except Exception as e:
            await update.callback_query.answer(
                text=TEXTS[lang].get("api_error", "Error connecting to service"),
                show_alert=True,
            )
            return INSTANT_PURCHASE_SERVER_ID


@is_user_banned
async def create_api_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create the order via API"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)

        try:
            provider = get_active_provider()
            api_provider = get_active_provider_enum()
            game_code = context.user_data.get("api_game_code")
            game_name = context.user_data.get("api_game_name", game_code)
            selected_denom = context.user_data.get("api_selected_denom", {})
            player_id = context.user_data.get("api_player_id")
            server_id = context.user_data.get("api_server_id")
            player_name = context.user_data.pop("api_player_name", None)

            denom_name = selected_denom.get("name", "")
            denom_price_usd = float(selected_denom.get("amount", 0))
            product_id = None
            try:
                product_id = (
                    int(selected_denom.get("id")) if selected_denom.get("id") else None
                )
            except (TypeError, ValueError):
                product_id = None

            exchange_rate = get_exchange_rate()
            denom_price_sudan = denom_price_usd * exchange_rate
            provider_logging.log_price_conversion(
                api_provider.value,
                "charge_user_balance",
                denom_name,
                denom_price_usd,
                "USD",
                user_id=update.effective_user.id,
                product_id=str(product_id) if product_id else None,
            )

            msg_target = update.message or (
                update.callback_query.message if update.callback_query else None
            )
            processing_msg = await msg_target.reply_text(
                text=TEXTS[lang].get("order_processing", "Processing order..."),
            )

            denomination = catalogue_to_denomination(selected_denom)
            remark = f"Order from Telegram Bot - User ID: {update.effective_user.id}"
            idempotency_key = str(uuid.uuid4())

            try:
                result = await provider.create_order(
                    game_code=game_code,
                    denomination=denomination,
                    player_id=player_id,
                    server_id=server_id,
                    remark=remark,
                    idempotency_key=idempotency_key,
                )
            except Exception as e:
                error_message = str(e)
                if (
                    "out of stock" in error_message.lower()
                    or "not available" in error_message.lower()
                    or "insufficient" in error_message.lower()
                    or "402" in error_message
                    or "409" in error_message
                ):
                    await processing_msg.edit_text(
                        text=TEXTS[lang].get(
                            "product_out_of_stock",
                            "This product is currently out of stock ❌\nWe apologize for the inconvenience",
                        ),
                    )
                else:
                    await processing_msg.edit_text(
                        text=TEXTS[lang]
                        .get("order_created_error", "Error creating order ❌\n{error}")
                        .format(error=error_message),
                    )
                return ConversationHandler.END

            if result.success and result.external_id:
                api_order_id = result.external_id
                api_message = result.message
                if result.player_name:
                    player_name = result.player_name

                from decimal import Decimal

                with models.session_scope() as s:
                    user = s.get(models.User, update.effective_user.id)
                    if not user:
                        await processing_msg.edit_text(
                            text=TEXTS[lang].get("error", "An error occurred ❌"),
                        )
                        return ConversationHandler.END

                    user.balance -= Decimal(str(denom_price_sudan))

                    api_order = models.ApiPurchaseOrder(
                        user_id=update.effective_user.id,
                        api_provider=api_provider,
                        api_order_id=api_order_id,
                        api_game_code=game_code,
                        product_id=product_id,
                        denomination_name=denom_name,
                        player_id=player_id,
                        player_name=player_name,
                        server_id=server_id,
                        price_usd=denom_price_usd,
                        price_sudan=denom_price_sudan,
                        status=(
                            models.ApiPurchaseOrderStatus.PROCESSING
                            if api_provider == models.ApiProvider.GAMEVOUCHERS
                            else models.ApiPurchaseOrderStatus.PENDING
                        ),
                        api_message=api_message,
                        remark=remark,
                    )
                    s.add(api_order)
                    s.commit()

                    order_text = (
                        TEXTS[lang]
                        .get(
                            "order_created_success",
                            "Order created successfully ✅\nOrder ID: {order_id}",
                        )
                        .format(order_id=api_order_id)
                    )
                    if selected_denom.get("delivery_mode") == "async":
                        order_text += "\n\n" + TEXTS[lang].get(
                            "order_async_hint",
                            "Your order is processing. You will be notified when it completes.",
                        )
                    order_details = (
                        TEXTS[lang]
                        .get(
                            "order_details",
                            (
                                "Order Details:\n"
                                "Game: {game_name}\n"
                                "Denomination: {denomination}\n"
                                "Price: {price}\n"
                                "Player ID: {player_id}\n"
                                "Current Balance: {balance}"
                            ),
                        )
                        .format(
                            game_name=escape_html(game_name),
                            denomination=escape_html(denom_name),
                            price=format_float(denom_price_sudan),
                            player_id=escape_html(player_id or "—"),
                            balance=format_float(user.balance),
                        )
                    )
                    order_text += f"\n\n{order_details}"

                await processing_msg.edit_text(text=order_text)
            else:
                error_msg = result.message or TEXTS[lang].get(
                    "api_error", "Error connecting to service"
                )
                if (
                    "out of stock" in error_msg.lower()
                    or "not available" in error_msg.lower()
                    or "insufficient" in error_msg.lower()
                ):
                    await processing_msg.edit_text(
                        text=TEXTS[lang].get(
                            "product_out_of_stock",
                            "This product is currently out of stock ❌\nWe apologize for the inconvenience",
                        ),
                    )
                else:
                    await processing_msg.edit_text(
                        text=TEXTS[lang]
                        .get("order_created_error", "Error creating order ❌\n{error}")
                        .format(error=error_msg),
                    )

            clear_instant_purchase_context(context)

            await msg_target.reply_text(
                text=TEXTS[lang].get("home_page", "Home Page 🔝"),
                reply_markup=build_user_keyboard(lang),
            )

        except Exception as e:
            error_msg = str(e)
            err_target = update.message or (
                update.callback_query.message if update.callback_query else None
            )
            if err_target:
                await err_target.reply_text(
                    text=TEXTS[lang]
                    .get("order_created_error", "Error creating order ❌\n{error}")
                    .format(error=error_msg),
                )
        return ConversationHandler.END


# Conversation handler
instant_purchase_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            instant_purchase,
            r"^instant_purchase$",
        ),
    ],
    states={
        INSTANT_PURCHASE_GAME: [
            CallbackQueryHandler(
                get_instant_purchase_game,
                r"^(api_game_|api_games_page_|api_search_page_)",
            ),
            MessageHandler(
                callback=handle_game_search,
                filters=filters.TEXT & ~filters.COMMAND,
            ),
        ],
        INSTANT_PURCHASE_DENOMINATION: [
            CallbackQueryHandler(
                get_instant_purchase_denomination,
                r"^(api_denom_|api_denoms_page_)",
            ),
        ],
        INSTANT_PURCHASE_PLAYER_ID: [
            MessageHandler(
                callback=get_instant_purchase_player_id,
                filters=filters.TEXT & ~filters.COMMAND,
            ),
        ],
        INSTANT_PURCHASE_SERVER_ID: [
            CallbackQueryHandler(
                get_instant_purchase_server_id,
                r"^api_server_",
            ),
        ],
        INSTANT_PURCHASE_CONFIRM: [
            CallbackQueryHandler(
                get_instant_purchase_confirm,
                r"^api_confirm_order$|^api_cancel_order$",
            ),
        ],
    },
    fallbacks=[
        start_command,
        admin_command,
        back_to_user_home_page_handler,
        CallbackQueryHandler(back_to_api_game, r"^back_to_api_game$"),
        CallbackQueryHandler(back_to_api_denom, r"^back_to_api_denom$"),
        CallbackQueryHandler(back_to_api_player_id, r"^back_to_api_player_id$"),
    ],
)
