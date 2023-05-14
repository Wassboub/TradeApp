import threading
import time
from binance.client import Client
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'
bot_token = '5835335312:AAFhKkx9s2mxtJQOGwLrpZZz2r7FXef9dm0'
chat_id = '-1001926020988'
client = Client(api_key, api_secret)  # Set timeout to 20 seconds
bot = telebot.TeleBot(bot_token)

# Semaphore for rate limiting API requests
api_semaphore = threading.Semaphore(value=20)


def get_coin_symbols():
    tickers = client.get_ticker()
    coin_symbols = {}

    for ticker in tickers:
        symbol = ticker['symbol']

        if symbol.endswith(('USDT','BUSD')):
            coin_symbols[symbol] = float(ticker['volume'])
    return coin_symbols


def process_coin(symbol, last_volume):
    ticker = client.get_ticker(symbol=symbol)
    new_volume = float(ticker['volume'])
    price = float(ticker['lastPrice'])

    if new_volume != 0:
        volume_change = (new_volume - last_volume) / last_volume

        if volume_change > 0.04:  # Volume change threshold of 4%
            message = f"🥏 Symbol: {symbol}\n"
            message += f"〽️ Last Price: {price}\n"
            message += f"📊 Volume Change: {round(volume_change * 100, 2)}%\n"
            threading.Thread(target=another_task, args=(symbol, message)).start()


def another_task(coin_name, message):
    with api_semaphore:
        trades = client.get_recent_trades(symbol=coin_name, limit=1000)

    buy_volume = sum(float(trade['qty']) for trade in trades if not trade['isBuyerMaker'])
    sell_volume = sum(float(trade['qty']) for trade in trades if trade['isBuyerMaker'])
    volume_ratio = buy_volume / sell_volume if sell_volume != 0 else 0

    message += f"🟢 Buy Volume: {round((buy_volume / (buy_volume + sell_volume)) * 100, 2)}%\n"
    message += f"🔴 Sell Volume: {round((sell_volume / (buy_volume + sell_volume)) * 100, 2)}%\n"

    if buy_volume > sell_volume:
        message += f"🟢🟢🟢 Positive Score: {round(volume_ratio, 2)}\n"
    else:
        message += f"🔴🔴🔴 Negative Score: {round(volume_ratio, 2)}\n"

    bot.send_message(chat_id, message)


def check_volume_changes():
    coin_volumes = get_coin_symbols()

    for symbol, last_volume in coin_volumes.items():
        process_coin(symbol, last_volume)


scheduler = BackgroundScheduler()
scheduler.add_job(check_volume_changes, 'interval', minutes=5,max_instances=10)  # Increase the max_instances value as needed
scheduler.start()

try:
    while True:
        bot.polling()
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
