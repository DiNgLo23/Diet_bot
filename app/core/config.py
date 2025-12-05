import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


REL_DB_PATH = os.getenv("DB_PATH")


DB_PATH = os.path.join(BASE_DIR, REL_DB_PATH)

