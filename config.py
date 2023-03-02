from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

TOKEN = getenv('TOKEN')

ACCESS_ID = getenv('ACCESS_ID')

CHANNEL_ID = getenv('CHANNEL_ID')

# webhook settings
WEBHOOK_HOST = getenv('WEBHOOK_HOST')
WEBHOOK_PATH = getenv('WEBHOOK_PATH')
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

# webserver settings
WEBAPP_HOST = getenv('WEBAPP_HOST')
WEBAPP_PORT = getenv('WEBAPP_PORT')

db = 'src/db/tg_markup.db'
