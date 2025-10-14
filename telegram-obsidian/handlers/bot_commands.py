from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from config import ADMINS
from create_bot import bot

# Импорт внутренних модулей
from keyboards.main_kb import main_menu_kb
from utils.list_notes import list_notes_tree

bot_commands_router = Router()  # Роутер для стартовых команд


# ==================== ОБРАБОТКА /start ====================
@bot_commands_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Инициализация меню"""
    if message.from_user.id in ADMINS:
        await message.answer("Добро пожаловать в бота Telegram Obsidian\n\n")

        await message.answer(
            "Выберите что вы хотите сделать",
            reply_markup=await main_menu_kb(),  # <-- Главное меню
        )


# ==================== ОБРАБОТКА /list ====================
@bot_commands_router.message(Command("list"))
async def list_notes(message: types.Message):
    """Вывод всех заметок в виде древа"""
    if message.from_user.id in ADMINS:
        notes_tree = await list_notes_tree()
        await message.answer(f"Вывод всех заметок в виде древа\n\n{notes_tree}")

        await bot.send_message(
            message.from_user.id,
            "Выберите что вы хотите сделать",
            reply_markup=await main_menu_kb(),
        )
