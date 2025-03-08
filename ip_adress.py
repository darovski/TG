import json
import requests
import asyncio
import http.client
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from pydantic.dataclasses import dataclass

from config import TOKEN, IP_API_KEY

# Получите токен бота из переменных окружения
API_TOKEN = TOKEN
IP_KEY = IP_API_KEY

# Инициализируйте бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для получения информации о диапазоне IP
def get_ip_range_info(ip):
    response = requests.get(f'https://ipinfo.io/{ip}?token=a72d661cbfead7'
    )
    data = response.json()
    print(data)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Хэндлер команды /start
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("Привет! Отправь мне IP-адрес, и я дам информацию о нем.")

# Хэндлер текстовых сообщений
@dp.message()
async def ip_info_handler(message: Message):
    ip_info = get_ip_range_info(message.text)

    if ip_info:
        response_text = f"Информация об IP:\n"
        ip = ip_info["ip"]
        hostname = ip_info["hostname"]
        city = ip_info["city"]
        region = ip_info["region"]
        country = ip_info["country"]
        loc = ip_info["loc"]
        org = ip_info["org"]
        postal = ip_info["postal"]
        timezone = ip_info["timezone"]


        await message.answer(f"{response_text}\n'IP адрес - '{ip}\n'Имя хоста - '{hostname}\n'Город - '{city}\n'Регион - '{region}\n'Страна - '{country}\n'Координаты - '{loc}\n'Организация - '{org}\n'Индекс - '{postal}\n'Часовой пояс - '{timezone}")
    else:
        response_text = "Не удалось получить информацию о диапазоне IP. Проверьте IP-адрес и попробуйте снова."

    #await message.answer(f'\n{ip_domain}\n{ip_name}\n{ip_url}')

# Запустите бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())