from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder  # Построитель клавиатур

# Соответствие внутренних названий подписок и их отображаемых имен


async def main_kb():
    """Создает клавиатуру для главного меню:
    - Позволяет создавать заметки и добавлять фото
    """
    builder = InlineKeyboardBuilder()

    # Кнопка возврата в главное меню
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(1)  # Вертикальное расположение кнопок

    return builder.as_markup()
