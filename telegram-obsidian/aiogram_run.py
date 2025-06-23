import asyncio
from aiogram.types import BotCommand
import locale

# Импорт основных компонентов проекта
from create_bot import bot, dp, setup_logger  # <-- Зависимость от конфигурации бота
from handlers.bot_commands import bot_commands_router  # <-- Роутер стартовых команд
from handlers.menu import menu_router  # <-- Роутер меню


async def setup_bot_commands(bot):
    """Настройка кнопки меню /start для пользователей"""
    bot_commands = [
        BotCommand(command="/start", description="Стартовая команда"),
        BotCommand(command="/list", description="Вывести все заметки"),
    ]
    await bot.set_my_commands(bot_commands)


async def main():
    """Главная функция инициализации:
    - Инициализация логгера
    - Настройка локализации
    - Подключение всех обработчиков
    - Запуск бота
    """
    try:
        # Инициализация логгера
        await setup_logger()

        # Важно: Локализация для корректного отображения дат/времени
        locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))

        # Подключение всех обработчиков из папки handlers
        dp.include_routers(  # <-- Центральная точка маршрутизации
            bot_commands_router,
            menu_router,
        )

        await bot.delete_webhook(drop_pending_updates=True)
        await setup_bot_commands(bot)
        await dp.start_polling(bot)  # <-- Основной цикл обработки сообщений
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await bot.session.close()  # Важно: Корректное завершение работы


if __name__ == "__main__":
    # Точка входа для запуска бота
    asyncio.run(main())
