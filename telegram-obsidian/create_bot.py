import logging
import config  # <-- Основные настройки проекта
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ==================== ЛОГГИРОВАНИЕ ====================
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)  # <-- Глобальный логгер для модуля


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
