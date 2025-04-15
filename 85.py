import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_mode = {}

@dp.message(CommandStart())
async def start(message: Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Высчитать НДС", callback_data="calc_nds")
    kb.button(text="Высчитать 70% и 30%", callback_data="calc_7030")
    kb.button(text="Высчитать 50%", callback_data="calc_50")
    kb.adjust(1)
    await message.answer("Выберите действие:", reply_markup=kb.as_markup())

@dp.callback_query(F.data.in_(["calc_7030", "calc_50", "calc_nds"]))
async def handle_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_mode[user_id] = callback.data
    await callback.message.answer("Введите число:")
    await callback.answer()

@dp.message()
async def handle_number(message: Message):
    user_id = message.from_user.id
    if user_id not in user_mode:
        await message.answer("Пожалуйста, сначала выберите действие с помощью /start")
        return

    try:
        number = float(message.text)
        mode = user_mode[user_id]
        if mode == "calc_nds":
            step1 = 12 / 112 * number
            result = step1
            text = (
                f"{number} = {result:.4f}\n"
            )
            await message.answer(text)
            
        elif mode == "calc_7030":
            step1 = number * 88 / 100
            step2 = step1 * 30 / 100
            result = step1 * 70 / 100
            result1 = result + step2
            text = (
                f"{number} - 12% = {step1}\n"
                f"30% от {step1}  = {step2:.4f}\n"
                f"70% от {step1} = {result:.4f}\n"
            )
            await message.answer(text)
            
        elif mode == "calc_50":
            step1 = number * 88 / 100
            result = step1 / 2
            text = (
                f"{number} - 12% = {step1:.4f}\n"
                f"{step1} / 2 = {result:.4f}\n"
                f"Результат: {result:.4f}"
            )
            await message.answer(text)
        else:
            result = "Неизвестный режим"
        await message.answer(f"Результат: {result}")
        
        del user_mode[user_id]
    except ValueError:
        await message.answer("Введите корректное число")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
