import botalive
import asyncio
from aiogram import Bot, Dispatcher


async def run():
    bot = Bot(token="token")
    dp = Dispatcher(bot=bot)
    monitoring = botalive.Monitoring(server_url="http://bot-alive.com/bots/monitoring", bot_name="TestBot",
                                     token="qosJWjssV8q0ZmnTvfL8Uw", run_async=True)

    @dp.message_handler(content_types=["text"])
    @monitoring.async_error_handler
    async def telegram_message_handler(message):
        await bot.send_message(chat_id="dsadsaddddddddddd", text=message.text)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(run())