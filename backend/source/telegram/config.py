from decouple import config

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
ADMIN_USERS = config('ADMIN_USERS')
HOST_URL = config('HOST_URL')
ADMIN_USERS = tuple(ADMIN_USERS[1:-1].split(', '))


