from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")
SQLITE_DB_FILE = Path(__file__).parent.parent.joinpath("store", "book-bot.sqlite3")
HAM_ON_RYE_TXT = Path(__file__).parent.parent.joinpath("store", "ham_on_rye.txt")
BOT_PROFILE_PICTURE = Path(__file__).parent.parent.joinpath("store", "book-bot.jpg")
