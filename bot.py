import os
import telebot
from flask import Flask, request
from dhan import DhanHQ

# === Load environment variables safely ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
DHAN_ENV = os.getenv("DHAN_ENV", "SANDBOX")  # Can be SANDBOX or LIVE

# === Initialize DhanHQ client ===
dhan = DhanHQ(env=DHAN_ENV, access_token=DHAN_ACCESS_TOKEN)

# === Initialize Telegram bot and Flask app ===
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# === Telegram Webhook Endpoint ===
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    return "OK", 200

# === Health check for Render ===
@app.route("/", methods=["GET"])
def index():
    return "✅ TradeCoPilot-K Bot is Running", 200

# === /start command ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello K! 👋 TradeCoPilot-K is online and connected to Dhan Sandbox!")

# === /status command ===
@bot.message_handler(commands=['status'])
def status(message):
    bot.send_message(message.chat.id, "🟢 Bot status: ONLINE\n📶 Dhan API: SANDBOX\n📊 Ready for trade logic...")

# === You can add more handlers like /bias, /trade, /news here ===

# === Entry point (for Render hosting) ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
