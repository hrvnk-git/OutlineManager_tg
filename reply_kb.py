from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class ButtonNames:
    ALL_KEYS = "Все ключи"
    ADD_KEY = "Добавить ключ"
    DEL_KEY = "Удалить ключ"


main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=ButtonNames.ALL_KEYS),
        ],
        [
            KeyboardButton(text=ButtonNames.ADD_KEY),
            KeyboardButton(text=ButtonNames.DEL_KEY),
        ],
    ],
    resize_keyboard=True,
)
