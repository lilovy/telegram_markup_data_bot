from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

# token to connect the bot
TOKEN = getenv('TOKEN')

# admin ID, for full access
ADMIN_ID = int(getenv('ADMIN_ID'))

# the list of id that are allowed
# to access the bot's functionality
ACCESS_ID = list(map(int, getenv('ACCESS_ID').split()))

# channel ID where files are saved
CHANNEL_ID = int(getenv('CHANNEL_ID'))

# webhook settings
WEBHOOK_HOST = getenv('WEBHOOK_HOST')
LOCALHOST = getenv('LOCALHOST')

WEBHOOK_PATH = f"/bot/{TOKEN}"

# webserver settings
WEBAPP_HOST = getenv('WEBAPP_HOST')
WEBAPP_PORT = getenv('WEBAPP_PORT')

WEBHOOK_URL = WEBAPP_HOST + WEBHOOK_PATH

# relative path to database
db_path = 'src/db/TGMarkup.db'
