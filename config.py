from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

TOKEN = getenv('TOKEN')

ADMIN_ID = int(getenv('ADMIN_ID'))

ACCESS_ID = list(map(int, getenv('ACCESS_ID').split()))

CHANNEL_ID = getenv('CHANNEL_ID')

# webhook settings
WEBHOOK_HOST = getenv('WEBHOOK_HOST')
LOCALHOST = getenv('LOCALHOST')

# WEBHOOK_PATH = getenv('WEBHOOK_PATH')
WEBHOOK_PATH = f"/bot/{TOKEN}"

# webserver settings
WEBAPP_HOST = getenv('WEBAPP_HOST')
WEBAPP_PORT = getenv('WEBAPP_PORT')

WEBHOOK_URL = WEBAPP_HOST + WEBHOOK_PATH

db_path = 'src/db/tg_markup.db'
