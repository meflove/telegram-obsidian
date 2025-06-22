from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram import types

# Импорт внутренних модулей
from keyboards.main_kb import main_kb

bot_commands_router = Router()  # Роутер для стартовых команд


# ==================== ОБРАБОТКА /start ====================
@bot_commands_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Инициализация меню:"""
    await message.answer(
        "Выберите что вы хотите сделать",
        reply_markup=await main_kb(),  # <-- Главное меню
    )


# ==================== ОБРАБОТКА /list ====================
@bot_commands_router.message(Command("list"))
async def calendar():
    """Вывод всех заметок в виде древа"""
    pass
