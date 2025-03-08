from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет")],
    [KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://dzen.ru/news")],
    [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru/home?tss=")],
    [InlineKeyboardButton(text="Видео", url="https://yandex.ru/video/search?from_block=efir_newtab&stream_channel=35&text=популярные+видео")],
])

inline_kb_dynamic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data='show_everyone')]
])

inline_kb_option = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data='option1')],
    [InlineKeyboardButton(text="Опция 2", callback_data='option2')]
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
   keyboard = ReplyKeyboardBuilder()
   for key in test:
        keyboard.add(KeyboardButton(text=key))
   return keyboard.adjust(2).as_markup()