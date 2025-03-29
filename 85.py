import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Введите число чтобы узнать свое стратегическое преимущесвто")

@dp.message()
async def handle_number(message: Message):
    try:
        number = float(message.text)
        result = number * 100 / 85
        await message.answer(f"Результат: {result}")
    except ValueError:
        await message.answer("Число не корректное")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

