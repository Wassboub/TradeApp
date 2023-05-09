from binance.client import Client
from datetime import datetime
import time
import telegram
import requests


# Set up API key and secret
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Connect to Binance's API
client = Client(api_key, api_secret)

# Initialize variables
buy_volume_15m = 0
sell_volume_15m = 0
buy_volume_1h = 0
sell_volume_1h = 0
buy_volume_4h = 0
sell_volume_4h = 0
processed_trade_ids = set()
processed_trade_ids2 = set()
period_length_15m = 900  # 15 minutes
period_length_1h = 3600  # 1 hour
period_length_4h = 14400  # 4 hours
periods_15m = [0] * 10  # Initialize periods list to keep track of net volumes for the last 10 periods
periods_1h = [0] * 10
periods_4h = [0] * 10
current_period_index = 0
# Reset the variables
buy_volume = 0
sell_volume = 0
bot_token = '6276656217:AAG2ULfvYbe-vito2JWHKYHBLpo__EuoZ1Q'
chat_id = '-1001965574985'
# Run the loop continuously
while True:
    try:
        # Retrieve the latest trades for the BTC/USDT pair
        trades = client.get_recent_trades(symbol='BTCUSDT', limit=800)
        # Calculate the total volume of executed large trades for buy and sell
        for trade in trades:
            if float(trade['qty']) > 0.1 and trade[ 'id'] not in processed_trade_ids:  # Trade volume threshold is set to 1 BTC and check if the trade has been processed before
             processed_trade_ids.add(trade['id'])  # Add the trade ID to the set of processed trades to avoid processing it again in the future

             if trade['isBuyerMaker']:  # Check if it's a buy or sell order
                    buy_volume += float(trade['qty'])

             else:
                  sell_volume += float(trade['qty'])

             if float(trade['qty']) > 10:
                 if trade['isBuyerMaker']:  # Check if it's a buy or sell order
                     message = f"🟢🟢 *whales just detected `{float(trade['qty']):.2f}` BTC\n"
                     requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                                   data={"chat_id": chat_id, "text": message})
                 else:
                     message = f"🔴🔴 *whales just detected `{float(trade['qty']):.2f}` BTC\n"
                     requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                                   data={"chat_id": chat_id, "text": message})
            if float(trade['qty']) > 0.01 and trade['id'] not in processed_trade_ids2:  # Trade volume threshold is set to 1 BTC and check if the trade has been processed before
                processed_trade_ids2.add(trade['id'])

                if trade['isBuyerMaker']:  # Check if it's a buy or sell order
                    buy_volume_4h += float(trade['qty'])
                    buy_volume_1h += float(trade['qty'])
                    buy_volume_15m += float(trade['qty'])
                else:
                    sell_volume_4h += float(trade['qty'])
                    sell_volume_1h += float(trade['qty'])
                    sell_volume_15m += float(trade['qty'])

        # Print the total volume of executed large trades for buy and sell
        if buy_volume > 30 or sell_volume > 30:
            print(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Large buy orders: {buy_volume:.2f} BTC, Large sell orders: {sell_volume:.2f} BTC")

            net_15m = periods_15m[-1]
            net_1h = periods_1h[-1]
            net_4h = periods_4h[-1]

            net_15m_emoji = "🟢" if net_15m > 0 else "🔴"
            net_1h_emoji = "🟢" if net_1h > 0 else "🔴"
            net_4h_emoji = "🟢" if net_4h > 0 else "🔴"

            message = f"🟢 *Large buy orders: `{buy_volume:.2f}` BTC*\n🟥 *Large sell orders: `{sell_volume:.2f}` BTC*\n{net_15m_emoji} last 15 min Netvolume: `{net_15m:.2f}` BTC*\n{net_1h_emoji} last 1 h Netvolume: `{net_1h:.2f}` BTC*\n{net_4h_emoji} last 4 h Netvolume: `{net_4h:.2f}` BTC*"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={"chat_id": chat_id, "text": message})

            # Reset the variables
        buy_volume = 0
        # Reset the variables
        buy_volume = 0
        sell_volume = 0
        if len(processed_trade_ids2) > 1000:
            processed_trade_ids2.clear()
        if len(processed_trade_ids) > 1000:
            processed_trade_ids.clear()



            # Calculate the net volume for the last 4 hours

        net_volume_4h =+ buy_volume_4h - sell_volume_4h
        net_volume_1h =+  buy_volume_1h - sell_volume_1h
        net_volume_15m=+  buy_volume_15m - sell_volume_15m
        print(net_volume_15m)
        # Update the periods lists with the net volume for the current periods
        periods_15m[current_period_index] = net_volume_15m
        periods_1h[current_period_index] = net_volume_1h
        periods_4h[current_period_index] = net_volume_4h

        # Increment the current period index and reset the variables if the current period has ended
        if time.time() >= (current_period_index + 1) * period_length_15m:
                current_period_index = (
                                                   current_period_index + 1) % 10  # Reset the current period index to keep the index within the range of 0 to 9
                buy_volume_15m = 0
                sell_volume_15m = 0
                periods_15m[current_period_index] = 0  # Reset the net volume for the current period to 0

        if time.time() >= (current_period_index + 1) * period_length_1h:
                current_period_index = (current_period_index + 1) % 10
                buy_volume_1h = 0
                sell_volume_1h = 0
                periods_1h[current_period_index] = 0

        if time.time() >= (current_period_index + 1) * period_length_4h:
                current_period_index = (current_period_index + 1) % 10
                buy_volume_4h = 0
                sell_volume_4h = 0
                periods_4h[current_period_index] = 0



        time.sleep(120)

    except Exception as e:
        print(e)
        time.sleep(150)  # Wait for 30 seconds before retrying if an exception occurs
