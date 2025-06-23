from logging import getLogger, StreamHandler, Formatter, WARNING, INFO
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config  # <-- Основные настройки проекта


# ==================== ЛОГГИРОВАНИЕ ====================
class ImmediateRotatingHandler(RotatingFileHandler):
    """Обработчик с немедленной записью для live-логирования"""

    def emit(self, record):
        super().emit(record)
        self.flush()  # Принудительный сброс буфера после каждой записи


async def setup_logger():
    logger = getLogger()
    logger.setLevel(INFO)

    # Форматирование с указанием времени в UTC
    formatter = Formatter(
        "[%(asctime)s UTC] %(levelname)-8s | %(name)-15s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Консольный вывод (stdout)
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    # Файловый вывод с live-записью
    file_handler = ImmediateRotatingHandler(
        filename="bot.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",  # Явное указание кодировки
    )
    file_handler.setFormatter(formatter)

    # Очистка предыдущих обработчиков
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Добавление новых обработчиков
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Фильтрация логов aiogram
    getLogger("aiogram").setLevel(INFO)
    getLogger("asyncio").setLevel(INFO)


# ==================== ЯДРО AIOGRAM ====================
bot = Bot(
    token=config.TOKEN,  # Токен из конфига
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN_V2
    ),  # Поддержка разметки
)

dp = Dispatcher(
    retry_after=5,  # Повторная обработка после ошибок через 5 сек
)
