import os
os.system("pip install telebot requests qrcode[Pill]")
import telebot
import requests

import qrcode
import time
#from dotenv import load_dotenv

#load_dotenv()

bot = telebot.TeleBot("8540881896:AAH_jeYaEFfN48ZqTao1LSSsAAH75NzN0dI")

@bot.message_handler(commands=["start"])
def start(m, res=False):
  #print(m)
  bot.send_message(m.chat.id, f'Привет {m.from_user.first_name}!\nЯ - QR-Code creation tool bot! Моя задача - облегчить создание QR-Кодов для пользователей!\n\nТебе стоит только отправить мне команду /qrcode и ссылку!\nИ я отправлю тебе qr-код максимально быстро!\n\nИспользуй /help для получения справки.')

@bot.message_handler(content_types=["text"])
def handle_text(message):
  message_text = message.text
  if message_text.lower() == "/help":
    bot.send_message(message.chat.id, "~ Меню помощи ~\n\n1. Используйте команду /qrcode <ссылка>, чтобы создать QR-Код.\n2. Если бот говорит о том что ссылка не верна, значит он не смог получить доступ к сайту, или формат ссылки не верный.\n3. Используйте /qrcode https://www.google.com/ чтобы проверить работоспособность бота.\n4. Если остались конкретные вопросы, предложения, и тд. свяжитесь с владельцем: @KILLER_DUROV.")
  if message_text.lower() == "/qrcode":
    bot.send_message(message.chat.id, "Использование: /qrcode <ссылка>")
    return
  if message_text.lower().startswith("/qrcode "):
    url = message_text[len("/qrcode "):]
    try:
        response = requests.get(url)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка! Не удалось получить информацию, или URL не верный!\nПроверьте правильность ссылки!")
        return
    if response.status_code != 200:
        bot.send_message(message.chat.id, "Ошибка! Не удалось получить информацию, или URL не верный!\nПроверьте правильность ссылки!")
        return
    bot_msg = bot.send_message(message.chat.id, "Ссылка получена, начинаю генерацию...")
    name = f"QRCode_{message.chat.id}_{time.time()}.png"
    try:
        qr = qrcode.make(url)
        qr.save(name)
        bot.delete_message(chat_id=message.chat.id, message_id=bot_msg.message_id)
        bot.send_photo(
            chat_id=message.chat.id,
            photo=open(name, "rb"),
            caption=f'Qr-code для <a href="{url}">ссылки</a> сгенерирован!',
            parse_mode='HTML'
        )
        os.remove(name)
    except Exception as e:
        print(e)
        try:
            os.remove(name)
        except Exception as e:
            pass
        bot.send_message(message.chat.id, "Ошибка создания!")


if __name__ == '__main__':
    print("Старт бота...")

    bot.polling(none_stop=True, interval=-0)
