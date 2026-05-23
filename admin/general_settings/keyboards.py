from telegram import InlineKeyboardButton
from common.lang_dicts import BUTTONS
import models
from models.ApiProvider import ApiProvider


def build_general_settings_keyboard(lang: models.Language = models.Language.ARABIC):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang].get("usd_to_sudan_rate", "USD to Sudan Rate"),
                callback_data="set_usd_to_sudan_rate",
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang].get("api_provider_settings", "API Provider"),
                callback_data="api_provider_settings",
            )
        ],
    ]
    return keyboard


def build_api_provider_keyboard(
    current: ApiProvider, lang: models.Language = models.Language.ARABIC
):
    g2_label = BUTTONS[lang].get("api_provider_g2bulk", "G2Bulk")
    gv_label = BUTTONS[lang].get("api_provider_gamevouchers", "Game Vouchers")
    if current == ApiProvider.G2BULK:
        g2_label = f"✅ {g2_label}"
    else:
        gv_label = f"✅ {gv_label}"
    return [
        [
            InlineKeyboardButton(
                text=g2_label,
                callback_data="set_api_provider_g2bulk",
            )
        ],
        [
            InlineKeyboardButton(
                text=gv_label,
                callback_data="set_api_provider_gamevouchers",
            )
        ],
    ]
