import logging
from logging.handlers import RotatingFileHandler
from config.settings import LOG_LEVEL, LOG_FILE

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, "INFO"),
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
    ]
)

logger = logging.getLogger("main_logger")
