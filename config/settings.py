import os

# ------------------------------
# General Settings
# ------------------------------

CSV_PATH = os.getenv("CSV_PATH", "data/dataset.csv")

DEFAULT_TABLE_NAME = os.getenv("DEFAULT_TABLE_NAME", "credit")

# ------------------------------
# Logging Settings
# ------------------------------

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOG_FILE = os.getenv("LOG_FILE", "app.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 5 * 1024 * 1024))  # 5 MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 3))

# ------------------------------
# API Keys
# ------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class AthenaConfig:
    DATABASE = "chatbot_athena_db"
    OUTPUT_LOCATION = "s3://chatbot-dados-analise/result/"