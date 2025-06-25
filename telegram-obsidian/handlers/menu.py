from aiogram import F, Router
from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

# Импорт внутренних модулей
from exceptions import NoteExists
from keyboards.main_kb import main_menu_kb
from utils.list_notes import list_notes_tree
from utils.notes_funcs import create_note

menu_router = Router()  # Роутер для стартовых команд


class CreateNote(StatesGroup):
    note_name = State()
    note_content = State()
    note_tags = State()


# ==================== ОБРАБОТКА call create_note ====================
@menu_router.callback_query(F.data == "create_note")
async def create_note_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNote.note_name)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_name")]
        ]
    )

    await call.message.answer("Введите название заметки:", reply_markup=keyboard)


# Обработчик пропуска названия (исправленное состояние)
@menu_router.callback_query(CreateNote.note_name, F.data == "skip_name")
async def skip_name_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(note_name=None)
    await state.set_state(CreateNote.note_content)

    await call.message.answer(
        "Название пропущено.\nВведите содержание заметки:", parse_mode=None
    )


# Обработчик ввода названия
@menu_router.message(CreateNote.note_name)
async def process_note_name(message: types.Message, state: FSMContext):
    await state.update_data(note_name=message.text)
    await state.set_state(CreateNote.note_content)

    await message.answer(
        f"Название сохранено: {message.text}\nТеперь введите содержание заметки:",
        parse_mode=None,
    )


# Обработчик ввода контента
@menu_router.message(CreateNote.note_content)
async def process_note_content(message: types.Message, state: FSMContext):
    await state.update_data(note_content=message.text)
    await state.set_state(CreateNote.note_tags)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пропустить", callback_data="skip_tags")]
        ]
    )

    await message.answer(
        f"Содержание сохранено: {message.text}\nТеперь введите теги заметки через пробел:",
        parse_mode=None,
        reply_markup=keyboard,
    )


# Обработчик пропуска тегов (исправленное состояние)
@menu_router.callback_query(CreateNote.note_tags, F.data == "skip_tags")
async def skip_tags_handler(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(note_tags=None)
    data = await state.get_data()

    try:
        await create_note(
            tags=[], name=data.get("note_name"), content=data.get("note_content")
        )

        await call.message.answer("Заметка создана!", parse_mode=None)
        await call.message.answer(
            "Выберите что вы хотите сделать",
            reply_markup=await main_menu_kb(),
        )
    except NoteExists as e:
        await call.message.answer(str(e), reply_markup=await main_menu_kb())

    await state.clear()


# Обработчик ввода тегов
@menu_router.message(CreateNote.note_tags)
async def process_note_tags(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tags = message.text.split() if message.text else []

    try:
        await create_note(
            tags=tags, name=data.get("note_name"), content=data.get("note_content")
        )
        await message.answer(f"Теги сохранены:\n{message.text}")
        await message.answer("Заметка создана!", parse_mode=None)
        await message.answer(
            "Выберите что вы хотите сделать",
            parse_mode=None,
            reply_markup=await main_menu_kb(),
        )
    except NoteExists as e:
        await message.answer(str(e))
        await message.answer(
            "Выберите что вы хотите сделать",
            reply_markup=await main_menu_kb(),
        )

    await state.clear()


@menu_router.callback_query(F.data == "list_notes")
async def list_notes_handler(call: types.CallbackQuery):
    tree = await list_notes_tree()
    try:
        await call.message.answer(tree, parse_mode=None)
    except TelegramBadRequest:
        await call.message.answer("Слишком много заметок!", parse_mode=None)

    await call.message.answer(
        "Выберите что вы хотите сделать",
        reply_markup=await main_menu_kb(),
    )
