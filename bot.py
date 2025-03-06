import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
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

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне /weather, и я пришлю тебе прогноз погоды в Екатеринбурге")

@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer('Умею: \n /start \n /help \n /weather Погода')

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

    except Exception as e:
        await message.reply('Произошла ошибка при получении данных о погоде.')
        logging.error(e)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())