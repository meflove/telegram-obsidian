from aiogram.utils.keyboard import InlineKeyboardBuilder  # Построитель клавиатур

# Соответствие внутренних названий подписок и их отображаемых имен


async def main_menu_kb():
    """Создает клавиатуру для главного меню:
    - Позволяет создавать заметки и добавлять фото
    """
    builder = InlineKeyboardBuilder()

    # Кнопка возврата в главное меню
    builder.button(text="📝 Создать заметку", callback_data="create_note")
    builder.button(text="🖨️ Вывести все заметки", callback_data="list_notes")
    builder.adjust(1)  # Вертикальное расположение кнопок

    return builder.as_markup()
