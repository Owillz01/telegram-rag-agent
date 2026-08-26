from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, html
import os
import logging as log
import asyncio
import sys

from retrival import answer_handler, get_faq

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
dp = Dispatcher()

conversation_history = {}

# dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message:Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    log.info("NESSAGE >>>:", message)
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}!')

def clear_conversation(user_id: int):
    if user_id in conversation_history:
        del conversation_history[user_id]
        log.info('deleted user with id: ', user_id)

@dp.message(Command('help'))
async def help_handler(message:Message) -> None:
    log.info(message)
    await message.answer(
        """
            Hi! I am your health bot. As much as I can, I will answer your health related queries.
        """
    )

@dp.message(Command("clear"))
async def clear_handler(message: Message) -> None:
    user_id = message.from_user.id
    clear_conversation(user_id)
    await message.answer("✅ Conversation history cleared! Starting fresh.")


@dp.message()
async def handle_rag(message:Message) -> None:
   user_id = message.from_user.id 
   user_msg = message.text

   print(f'User id: {user_id} msg: {user_msg}')

   try:
       if user_id not in conversation_history:
           conversation_history[user_id] = []

       conversation_history[user_id].append(f'Human: {user_msg}')

       rag_res = get_faq(user_msg)
       model_res = answer_handler(user_msg, rag_res)
       log.info(model_res, '<<<< MODEL RESPONSE')
       conversation_history[user_id].append(model_res)

       if len(conversation_history[user_id]) > 12:
           conversation_history[user_id] = conversation_history[user_id][-12]

       await message.answer(model_res)


   except Exception as e:
       print(f'Error Occured', e)
       await message.answer('Sorry an error occured!')
       

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Ensure webhook is removed before starting polling to avoid conflicts
    await bot.delete_webhook(drop_pending_updates=True)

    # And the run events dispatching
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    log.basicConfig(level=log.INFO, stream=sys.stdout)
    print('running')
    log.info('---NOW RUNNING')
    asyncio.run(main())