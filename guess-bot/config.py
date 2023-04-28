from os import getenv

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")
SQLITE_DB_FILE = Path(__file__).parent.joinpath("guess-bot.sqlite3")
