from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from bot.utils.i18n import t


def main_menu_keyboard(lang: str = "uz", is_admin: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text=t("btn_catalog", lang)),
            KeyboardButton(text=t("btn_cart", lang)),
        ],
        [
            KeyboardButton(text=t("btn_orders", lang)),
            KeyboardButton(text=t("btn_ai_sales", lang)),
        ],
        [
            KeyboardButton(text=t("btn_about", lang)),
            KeyboardButton(text=t("btn_contact", lang)),
        ],
        [
            KeyboardButton(text=t("btn_lang", lang)),
        ]
    ]
    if is_admin:
        buttons.append([KeyboardButton(text=t("btn_admin_panel", lang))])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Quyidagilardan birini tanlang..."
    )


def contact_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_send_contact", lang), request_contact=True)],
            [KeyboardButton(text=t("btn_cancel", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def location_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_send_location", lang), request_location=True)],
            [KeyboardButton(text=t("btn_cancel", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def cancel_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_cancel", lang))]
        ],
        resize_keyboard=True
    )


def payment_methods_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("payment_cash", lang))],
            [KeyboardButton(text=t("payment_click", lang)), KeyboardButton(text=t("payment_payme", lang))],
            [KeyboardButton(text=t("btn_cancel", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
