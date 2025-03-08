import logging
import asyncio
import requests
import os

import keyboards as kb

from aiogram.enums import ParseMode
from gtts import gTTS
from googletrans import Translator
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from config import API_KEY, API_URL, TOKEN

# Вставьте сюда ваш токен Telegram-бота
TELEGRAM_TOKEN = TOKEN

# Вставьте сюда ваш ключ API для прогноза погоды
WEATHER_API_KEY = API_KEY
WEATHER_API_URL = API_URL

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@dp.callback_query(F.data == 'show_everyone')
async def show_everyone(callback: CallbackQuery):
   await callback.message.edit_text('show_everyone', reply_markup=kb.inline_kb_option)

@dp.callback_query(F.data == 'option1')
async def option1(callback: CallbackQuery):
   await callback.message.answer('Опция1')

@dp.callback_query(F.data == 'option2')
async def option2(callback: CallbackQuery):
   await callback.message.answer('Опция2')

@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.reply("Привет! Отправь мне /weather, и я пришлю тебе прогноз погоды в Екатеринбурге", reply_markup=kb.main)

@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer('Умею: \n /start \n /help \n /weather Погода')

@dp.message(F.text == "Привет")
async def test_button(message: Message):
   await message.answer(f'Привет, {message.from_user.first_name}')

@dp.message(F.text == "Пока")
async def test_button(message: Message):
   await message.answer(f'До свидания, {message.from_user.first_name}')

@dp.message(Command('links'))
async def send_welcome(message: Message):
    await message.reply("Вот тебе ссылки", reply_markup=kb.inline_kb)

@dp.message(Command('dynamic'))
async def test_button(message: Message):
    await message.answer("Показать больше", reply_markup=kb.inline_kb_dynamic)

@dp.message(F.photo)
async def react_photo(message: Message):
    msg = ('Хорошая картинка, сохранил себе!')
    await message.answer(msg)
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(Command('weather'))
async def get_weather(message: types.Message):
    city = 'Екатеринбург'

    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        weather_data = response.json()

        if weather_data.get('cod') != 200:
            await message.reply(f"Не удалось получить данные о погоде для города {city}.")
            return

        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        await message.reply(f"Погода в {city}: {description}, температура: {temp}°C")

        rand_training = (f"Погода в {city}: {description}, температура: {temp}°C")

        tts = gTTS(text=rand_training, lang='ru')
        tts.save("weather.ogg")
        audio = FSInputFile("weather.ogg")
        await bot.send_voice(chat_id=message.chat.id, voice=audio)
        os.remove("weather.ogg")

    except Exception as e:
        await message.reply('Произошла ошибка при получении данных о погоде.')
        logging.error(e)

@dp.message()
async def translate_message(message: types.Message):
    translator = Translator()
    translated = translator.translate(message.text, dest='en')
    await message.reply(translated.text, parse_mode=ParseMode.MARKDOWN)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())