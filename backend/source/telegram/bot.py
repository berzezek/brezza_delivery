import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN

from handlers import (
    delivery_bot,
    admin_bot,
)

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def main():

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(delivery_bot.router)
    dp.include_router(admin_bot.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    print('Starting bot...')
    asyncio.run(main())
