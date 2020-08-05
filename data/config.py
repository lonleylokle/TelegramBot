import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
]

WEBAPP_HOST = os.getenv("WEBAPP_HOST")
WEBAPP_PORT = os.getenv("WEBAPP_PORT")

WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = str(os.getenv("WEBHOOK_PATH"))
WEBHOOK_URL=f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBHOOK_SSL_CERT = str(os.getenv("WEBHOOK_SSL_CERT"))
WEBHOOK_SSL_PRIV = str(os.getenv("WEBHOOK_SSL_PRIV"))

aiogram_redis = {
    'host': WEBAPP_HOST,
}

redis = {
    'address': (WEBAPP_HOST, 6379),
    'encoding': 'utf8'
}
