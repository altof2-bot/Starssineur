
import os
import time
from bot import bot

def main():
    while True:
        try:
            print("🤖 Bot Telegram démarré...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Erreur: {e}")
            time.sleep(3)
            continue

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    main()
