# from dotenv import load_dotenv
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message
# from aiogram import Bot, Dispatcher, html
# import os
# import logging as log
# import asyncio
# import sys

# load_dotenv()

# BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
# dp = Dispatcher()

# async def main() -> None:
#     bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

#     # Ensure webhook is removed before starting polling to avoid conflicts
#     await bot.delete_webhook(drop_pending_updates=True)

#     # And the run events dispatching
#     await dp.start_polling(bot, skip_updates=False)


# if __name__ == "__main__":
#     log.basicConfig(level=log.INFO, stream=sys.stdout)
#     print('running')
#     log.info('---NOW RUNNING')
#     asyncio.run(main())