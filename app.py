import os
import threading
from flask import Flask
from bot import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
