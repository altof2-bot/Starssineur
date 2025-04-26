# keep_alive.py
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run():
    # Render ou Koyeb exposent le port via la variable d'environnement PORT
    port = int(__import__('os').environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
