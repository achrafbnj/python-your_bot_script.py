import ccxt
import talib
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Initialize the Telegram bot
updater = Updater(token='6723919110:AAF1GB2qAT4pfdJjLoXZV-HDrcdBsazE2NU', use_context=True)
dispatcher = updater.dispatcher

# Function to fetch historical price data
def fetch_data(symbol, timeframe='1d', limit=200):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Function to calculate technical indicators
def calculate_indicators(df):
    df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)
    df['SMA_200'] = talib.SMA(df['close'], timeperiod=200)
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    df['MACD'], df['MACD_signal'], _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df

# Function to generate buy and sell signals
def generate_signals(df):
    df['Buy_Signal'] = np.where((df['SMA_50'] > df['SMA_200']) & (df['RSI'] < 30) & (df['MACD'] > df['MACD_signal']), 1, 0)
    df['Sell_Signal'] = np.where((df['SMA_50'] < df['SMA_200']) & (df['RSI'] > 70) & (df['MACD'] < df['MACD_signal']), -1, 0)
    return df

# Command handler for /analyze command
def analyze(update, context):
    coin_name = context.args[0]
    data = fetch_data(f'{coin_name}/USDT')  # Assuming the coin is traded against USDT
    data = calculate_indicators(data)
    data = generate_signals(data)
    
    # Send the analysis results back to the user
    update.message.reply_text(f'Analysis for {coin_name}:\n'
                              f'Buy signals: {data[data["Buy_Signal"] == 1].index}\n'
                              f'Sell signals: {data[data["Sell_Signal"] == -1].index}')

# Handler for unknown commands
def unknown(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")

# Add command handlers to the dispatcher
analyze_handler = CommandHandler('analyze', analyze)
dispatcher.add_handler(analyze_handler)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Start the bot
updater.start_polling()
updater.idle()
