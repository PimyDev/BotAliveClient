# BotAliveClient
 Library for monitoring bots using @botalive_bot
 
# Getting started
### Initialization of the monitoring object
 ```python
 import botalive
 
 monitoring = botalive.Monitoring(server_url="http://bot-alive.com/bots/monitoring", bot_name="TestBot",
                                     token="qosJWjssV8q0ZmnTvfL8Uw1", run_async=True)
 ```
 
 
This code will create a monitoring object that will work in asynchronous

Arguments:    
   server_url (str): Url to which the request will go  
   bot_name (str): The name of the bot that will be displayed in the notification  
   token (str): Token for this ip  
   run_async (bool): async or sync bot  
   
### Setup handler

Example using aiogram

 ```python
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
 ```
 
 **async_error_handler** decorator for async libraries  
 **sync_error_handler** decorator for sync libraries
