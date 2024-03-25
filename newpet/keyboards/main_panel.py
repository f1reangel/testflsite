from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_panel_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Почати анкетування✍",callback_data="start_survey")
    kb.button(text="Видалити дані про мене 🗑")
    kb.button(text="Вийти з бота🚪")
    kb.adjust(1, 2)
    return kb.as_markup(resize_keyboard=True)


def get_number_user() -> ReplyKeyboardMarkup:
    test_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Ваш номер телефону: ☎️", request_contact=True),
            ],
        ],
        resize_keyboard=True,
)
    return test_kb
