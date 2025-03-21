import os
import time
import threading
from flask import Flask
from bot import bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def start_bot():
    while True:
        try:
            print("🤖 Bot Telegram démarré...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Erreur: {e}")
            time.sleep(3)

if __name__ == "__main__":
    # Démarrer le bot Telegram dans un thread séparé
    threading.Thread(target=start_bot).start()

    # Lancer le serveur Flask pour Koyeb
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)