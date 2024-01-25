import os

from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_AUDIO = os.getenv("S3_BUCKET_AUDIO")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_NAME = os.getenv("DB_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LANGUAGES_ACRONYMS = {
    "jp": "Japanese",
    "en": "English",
}
