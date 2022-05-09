import configparser
import logging

import telegram
from flask import Flask, request
from telegram.ext import CommandHandler, Dispatcher, MessageHandler
import os

# Load data from config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
logger.debug(os.environ)

TELEGRAM_ACCESS_TOKEN = os.environ.get("TELEGRAM_ACCESS_TOKEN")
if not TELEGRAM_ACCESS_TOKEN: # If no available, then defined in local file.
    TELEGRAM_ACCESS_TOKEN = config["TELEGRAM"]["TELEGRAM_ACCESS_TOKEN"]

bot = telegram.Bot(token=(TELEGRAM_ACCESS_TOKEN))

# Bot Logic
@app.route("/hook", methods=["POST"])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return "ok"


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Kedroid bot is coming to live.")


def _parse_tg_command(text):
    pass

############################################################

# New a dispatcher for bot
dispatcher = Dispatcher(bot, True)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
