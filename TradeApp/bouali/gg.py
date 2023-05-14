from binance.client import Client
from datetime import datetime
import time
import requests

last_reset_time15m = datetime.now()
last_reset_time1h = datetime.now()
last_reset_time4h = datetime.now()
last_reset_time1d = datetime.now()
last_reset_time3d = datetime.now()
# Set up API key and secret
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Connect to Binance's API
client = Client(api_key, api_secret)

# Initialize variables

processed_trade_ids = set()
processed_trade_ids2 = set()
net_volume_affiche_4h = 0
net_volume_affiche_1h = 0
net_volume_affiche_15m = 0
net_volume_affiche_1d = 0
net_volume_affiche_3d = 0
net_volume_4h = 0
net_volume_1h = 0
net_volume_15m = 0
net_volume_1d = 0
net_volume_3d = 0

# Reset the variables
buy_volume = 0
sell_volume = 0
bot_token = '6276656217:AAG2ULfvYbe-vito2JWHKYHBLpo__EuoZ1Q'
chat_id = '-1001965574985'
# Run the loop continuously
while True:

    try:

        # Retrieve the latest trades for the BTC/USDT pair
        trades = client.get_recent_trades(symbol='BTCUSDT', limit=1000)
        # Calculate the total volume of executed large trades for buy and sell
        for trade in trades:

            print(trade)
            if float(trade['qty']) > 0.01 and trade['id'] not in processed_trade_ids2:
                processed_trade_ids2.add(trade['id'])

                if trade['isBuyerMaker']:  # Check if it's a buy or sell order
                    net_volume_4h += float(trade['qty'])
                    net_volume_1h += float(trade['qty'])
                    net_volume_15m += float(trade['qty'])
                    net_volume_1d += float(trade['qty'])
                    net_volume_3d += float(trade['qty'])
                else:
                    net_volume_4h -= float(trade['qty'])
                    net_volume_1h -= float(trade['qty'])
                    net_volume_15m -= float(trade['qty'])
                    net_volume_1d -= float(trade['qty'])
                    net_volume_3d -= float(trade['qty'])
            if float(trade['qty']) > 0.1 and trade['id'] not in processed_trade_ids:  # Trade volume threshold is set to 1 BTC and check if the trade has been processed before
             processed_trade_ids.add(trade['id'])  # Add the trade ID to the set of processed trades to avoid processing it again in the future

             if trade['isBuyerMaker']:  # Check if it's a buy or sell order
                    buy_volume += float(trade['qty'])

             else:
                  sell_volume += float(trade['qty'])

             if float(trade['qty']) > 10:
                 if trade['isBuyerMaker']:  # Check if it's a buy or sell order
                     message = f"🐳🟢 BUY WHALES DETECTED [ {float(trade['qty']):.2f}] BTC\n"
                     requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                                   data={"chat_id": chat_id, "text": message})
                 else:
                     message = f"🐳🔴 SELL WHALES DETECTED [ {float(trade['qty']):.2f}] BTC\n"
                     requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                                   data={"chat_id": chat_id, "text": message})



        if buy_volume > 30 or sell_volume > 30:
            print(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Large buy orders: {buy_volume:.2f} BTC, Large sell orders: {sell_volume:.2f} BTC")




            net_15m_emoji = "✳️" if net_volume_affiche_15m > 0 else "⛔️"
            net_1h_emoji = "✳️" if net_volume_affiche_1h > 0 else "⛔️"
            net_4h_emoji = "✳️" if net_volume_affiche_4h > 0 else "⛔️"
            net_1d_emoji = "✳️" if net_volume_affiche_1d > 0 else "⛔️"
            net_3d_emoji = "✳️" if net_volume_affiche_3d > 0 else "⛔️"

            message = f"🟢 BUY ORDRES  : ({buy_volume:.2f}) BTC\n 🔴 SELL ORDERS: ({sell_volume:.2f}) BTC \n {net_15m_emoji} 15 min Net: ({net_volume_affiche_15m:.2f}) BTC\n{net_1h_emoji}  1 h Net: ({net_volume_affiche_1h:.2f}) BTCBTC\n{net_4h_emoji}  4 h Net: ({net_volume_affiche_4h:.2f}) BTC"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={"chat_id": chat_id, "text": message})

            # Reset the variables
        buy_volume = 0
        sell_volume = 0
        if len(processed_trade_ids2) > 5000:
            my_list = list(processed_trade_ids2)
            half_list = my_list[len(my_list) // 2:]
            processed_trade_ids2 = set(half_list)

        if len(processed_trade_ids) > 5000:
            my_list = list(processed_trade_ids)
            half_list = my_list[len(my_list) // 2:]
            processed_trade_ids = set(half_list)

        current_time = datetime.now()
        print(net_volume_1h,net_volume_4h)
        net_15m_emoji = "🟢" if net_volume_affiche_15m > 0 else "🔴"
        net_1h_emoji = "🟢" if net_volume_affiche_1h > 0 else "🔴"
        net_4h_emoji = "🟢" if net_volume_affiche_4h > 0 else "🔴"
        net_1d_emoji = "🟢" if net_volume_affiche_1d > 0 else "🔴"
        net_3d_emoji = "🟢" if net_volume_affiche_3d > 0 else "🔴"

        if (current_time - last_reset_time1h).total_seconds() >= 60 * 60:
            # Reset the variable to 0 and update the last reset time
            last_reset_time1h = current_time
            net_volume_affiche_1h = net_volume_1h

            message = f"In the last 1 h  theNetFlow for btc is : {net_1h_emoji} {net_volume_affiche_1h:.2f} BTC"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={"chat_id": chat_id, "text": message})
            net_volume_1h=0
        if (current_time - last_reset_time4h).total_seconds() >= 4 * 60 * 60:
            # Reset the variable to 0 and update the last reset time
            net_volume_affiche_4h = net_volume_4h
            net_volume_4h = 0
            last_reset_time4h = current_time
            message = f"In the last 4 h  theNetFlow for btc is : {net_4h_emoji} {net_volume_affiche_4h:.2f} BTC"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                              data={"chat_id": chat_id, "text": message})


        if (current_time - last_reset_time15m).total_seconds() >= 15 * 60:
            # Reset the variable to 0 and update the last reset time
            net_volume_affiche_15m = net_volume_15m
            net_volume_15m = 0
            last_reset_time15m = current_time
        if (current_time - last_reset_time1d).total_seconds() >= 60*24* 60:
            # Reset the variable to 0 and update the last reset time
            net_volume_affiche_1d = net_volume_1d
            net_volume_1d = 0
            last_reset_time1d = current_time
            message = f"In the last 24 h  theNetFlow for btc is : {net_1d_emoji} {net_volume_affiche_1d:.2f} BTC"
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={"chat_id": chat_id, "text": message})

        if (current_time - last_reset_time1d).total_seconds() >= 180 * 24 * 60:
                # Reset the variable to 0 and update the last reset time
                net_volume_affiche_3d = net_volume_3d
                net_volume_3d = 0
                last_reset_time1d = current_time
                message = f"In the last 3 days  theNetFlow for btc is : {net_3d_emoji} {net_volume_affiche_3d:.2f} BTC"
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                      data={"chat_id": chat_id, "text": message})
        time.sleep(220)

    except Exception as e:
        print(e)
        time.sleep(180)  # Wait for 30 seconds before retrying if an exception occurs
