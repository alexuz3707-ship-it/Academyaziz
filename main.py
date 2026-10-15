import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

TOKEN = "8781257605:AAEu617n5YQqVMb9sKvY61w4j1ud8tWqL-Y"
WEB_APP_URL = "https://alexuz3707-ship-it.github.io/Akademyaziz/"

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[[
          InlineKeyboardButton(
              text="🎓 Azizbek Turg'unboyev Academy Panel",
              web_app=WebAppInfo(url=WEB_APP_URL),
          )
      ]]
  )

  await message.answer(
      "Assalomu alaykum!\n\n"
      "**Azizbek Turg'unboyev Academy** tizimiga xush kelibsiz.\n"
      f"Sizning Telegram Chat ID: `{message.chat.id}`\n\n"
      "Tizim panelini ochish uchun quyidagi tugmani bosing:",
      reply_markup=keyboard,
      parse_mode="Markdown",
  )


@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
  try:
    data = json.loads(message.web_app_data.data)
    action = data.get("action")

    if action == "attendance_notification":
      full_name = data.get("full_name")
      subject = data.get("subject")
      status = data.get("status")
      target_chat_id = data.get("telegram_id")

      if status == "keldi":
        msg_text = (
            f"Assalomu alaykum! Bugun {full_name} o'quvchimiz {subject} darsiga"
            " keldi, siz xotirjam bo'ling."
        )
      else:
        msg_text = (
            f"Diqqat! Bugun {full_name} o'quvchimiz {subject} darsiga KELMADI."
        )

      if target_chat_id:
        try:
          await bot.send_message(chat_id=target_chat_id, text=msg_text)
        except Exception:
          pass

      await message.answer(
          f"📩 Bildirishnoma saqlandi va jo'natildi:\n{msg_text}"
      )

    elif action == "homework_notification":
      group = data.get("group")
      subject = data.get("subject")
      task = data.get("task")

      homework_msg = (
          f"📚 **{subject} fanidan yangi vazifa/test joylandi!**\n"
          f"👥 Guruh: {group}\n"
          f"📝 Bugungi vazifangiz: {task}\n\n"
          f"Iltimos, Web App paneliga kirib fayllarni ko'rib chiqing va"
          f" bajarishingizni so'raymiz."
      )

      await message.answer(homework_msg, parse_mode="Markdown")

  except Exception as e:
    await message.answer(f"Xatolik: {e}")


async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
