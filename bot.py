import os
import telebot
import requests

BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Кидай мне финальную ссылку с кодом, и я попробую её вытащить.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    if not url.startswith('http'):
        bot.reply_to(message, "Это не похоже на ссылку. Отправь полный URL.")
        return

    msg = bot.reply_to(message, "⏳ Обрабатываю ссылку, подожди...")

    try:
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=15)
        data = response.json()

        if data.get('status') == 'success':
            result_url = data.get('result')
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, 
                                  text=f"✅ Готово!\n\nТвоя ссылка:\n{result_url}")
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, 
                                  text="❌ Не удалось обойти ссылку. API перегружено.")
            
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, 
                              text="⚠️ Ошибка при обработке. Попробуй позже.")
