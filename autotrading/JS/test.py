import telegram
import asyncio


async def telegram_send(text): #실행시킬 함수명 임의지정
    chat_id = 6067152407
    token = "7449204335:AAGhIXcV8x1I8TRrB-yKG-UoXZ7YxPJyN9s"
    bot = telegram.Bot(token = token)
    await bot.send_message(chat_id,text)

asyncio.run(telegram_send()) #봇 실행하는 코드