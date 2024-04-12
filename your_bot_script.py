import logging
import telegram
from telegram.ext import Updater, CommandHandler
import talib
import requests

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = '6723919110:AAF1GB2qAT4pfdJjLoXZV-HDrcdBsazE2NU'

# Initialize the bot
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    update.message.reply_text('Welcome to the Coin Analysis Bot! Please send me the name of the coin you want to analyze.')

def analyze_coin(update, context):
    coin_name = update.message.text
    chat_id = update.message.chat_id
    
    # Fetch historical data for the coin (You'll need to replace this with your actual API call)
    url = f' https://pro-api.coinmarketcap.com/v1/cryptocurrency/airdrop '
    response = requests.get(url)
    data = response.json()
    close_prices = [entry[1] for entry in data['prices']]
    
    # Perform analysis
    # Example: Simple Moving Average (SMA) for 14 periods
    sma = talib.SMA(close_prices, timeperiod=14)
    
    # Example: Relative Strength Index (RSI) for 14 periods
    rsi = talib.RSI(close_prices, timeperiod=14)
    
    # Example: Bollinger Bands (BBANDS) for 20 periods, 2 standard deviations
    upperband, middleband, lowerband = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    
    # Example: Fibonacci Retracement Levels
    fib_levels = talib.FIB(close_prices)
    
    # Send analysis to the user
    message = f"Analysis for {coin_name}:\n"
    message += f"SMA(14) = {sma[-1]}\n"
    message += f"RSI(14) = {rsi[-1]}\n"
    message += f"Upper Bollinger Band = {upperband[-1]}\n"
    message += f"Middle Bollinger Band = {middleband[-1]}\n"
    message += f"Lower Bollinger Band = {lowerband[-1]}\n"
    message += f"Fibonacci Retracement Levels = {fib_levels[-1]}\n"
    
    bot.send_message(chat_id=chat_id, text=message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('analyze', analyze_coin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
