import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
WECHAT_TOKEN: str = os.getenv("WECHAT_TOKEN", "")
BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
