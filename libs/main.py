import telebot
from LongOnlyTrader import LongOnlyTrader
import os

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN_TEST')
api_key = os.environ.get('BINANCE_API_KEY_TEST')
api_secret = os.environ.get('BINANCE_API_SECRET_TEST')
symbol = "BTCUSDT"
bar_length = "1m"
return_thresh = 0
volume_thresh = [-3, 3]
units = 0.01
position = 0

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    trader = LongOnlyTrader(
        symbol=symbol,
        bar_length=bar_length,
        return_thresh=return_thresh,
        volume_thresh=volume_thresh,
        units=units,
        position=position,
        api_key=api_key,
        api_secret=api_secret,
        bot=bot,
        message_callback=bot.send_message,
        chat_id=message.chat.id
    )

    trader.start_trading(historical_days=1/24)

bot.infinity_polling()


