from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")
SQLITE_DB_FILE = Path(__file__).parent.parent.joinpath("store", "book-bot.sqlite3")
SQLITE_SCRIPT = Path(__file__).parent.parent.joinpath("database", "book-bot.sql")
HAM_ON_RYE_TXT = Path(__file__).parent.parent.joinpath("store", "ham_on_rye.txt")
HAM_ON_RYE_JSON = Path(__file__).parent.parent.joinpath("store", "ham_on_rye.json")
