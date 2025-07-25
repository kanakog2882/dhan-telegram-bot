from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Dhan Telegram Bot is Running"

if __name__ == '__main__':
    app.run()
