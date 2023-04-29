from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required 
from django.shortcuts import HttpResponseRedirect
from Trade.forms import LoginForm, CoinForm
from .models import CoinInfo, CoinInfo_2
from .model_view import Alert
import csv
from datetime import datetime
import os
from binance.client import Client
import random
import string
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
from requests.exceptions import ReadTimeout
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)
exchange_info = client.get_exchange_info()
usdtpair=[]

@permission_required('is_superuser')
@login_required(login_url="/signin")
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url="/signin")
def home_1_scalp(request): 
    coinsInfos = CoinInfo.objects.order_by('-Time')[:1500]
    return render(request, 'home_1_scalp.html', {"coinsInfo" : coinsInfos})

@login_required(login_url="/signin")
def home_2_swing(request): 
    coinsInfos = CoinInfo_2.objects.all().order_by('-Time')
    return render(request, 'home_2_swing.html', {"coinsInfo" : coinsInfos})
   
@login_required(login_url="/signin")
def home_3_btc(request): 
    coinsInfos = CoinInfo_2.objects.all().order_by('-Time')
    return render(request, 'home_3_btc.html', {"coinsInfo" : coinsInfos})

@login_required(login_url="/signin")
def home_4_history(request):
     if request.method == 'POST':
        
        form = CoinForm(request.POST)
        if request.POST['Coin'] != "":
            symbol = request.POST['Coin']
            alerts = getConformeData(echo_message(symbol))
            print("-*-*-*-*--*-*-*-*-*-*-*-*")
            print("*************************")
            plot_dt = plot_data(alerts)
            print("-------------------------")
            X= plot_date2(alerts)
            plot_lb = plot_date(alerts)
            date = datetime.strptime('08/12/2022 18:35',  '%d/%m/%Y %H:%M')
            return render(request, 'home_4_history.html', {"plot_date": plot_lb ,"plot_data": plot_dt,"plot_data2": X ,"alerts" : alerts , "Symbol": symbol , "date": date,'form': form})
        else:
            return render(request, 'home_4_history.html', {'form': form, 'notif':'Coin not exist'})
     else:
        form = CoinForm(request.POST)
        symbol = "---"
        return render(request, 'home_4_history.html', {'form': form, "Symbol": symbol})
     
   
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home_1_scalp.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            msg = 'Error Login'
            form = LoginForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')


def getcoin(coin,path):
    #print("getcoin")
    y = []
    with open(path) as file:
        reader = csv.reader(file)
        for x in reader:
            y.append(str(x).split("\\t"))
    for x in range(len(y)):
        y[x][6] = y[x][6][:len(y[x][6]) - 2]
        y[x][0] = y[x][0][2:]

    return y

def echo_message(message):
    binance_data = BinanceData()
    # Fetch data for BTC/USDT pair
    df = binance_data.fetch_data(message)
    return df

class BinanceData:
    def __init__(self):
        self.client = Client("", "")
        self.directory = 'binance_data'
        self.interval = Client.KLINE_INTERVAL_5MINUTE
        self.start_ts = int(datetime.timestamp(datetime.now() - timedelta(days=5)))
        self.end_ts = int(datetime.timestamp(datetime.now()))

    def fetch_data(self, symbol):
        try:
            # Fetch historical klines for the given symbol
            klines = self.client.get_historical_klines(symbol, self.interval, self.start_ts * 1000, self.end_ts * 1000)
        except ReadTimeout as e:
            raise Exception(f'Request timed out for {symbol}. Skipping...') from e

        # Convert klines to pandas dataframe
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                           'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                           'taker_buy_quote_asset_volume', 'ignore'])

        # Convert timestamp to datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # Set timestamp as index
        df.set_index('timestamp', inplace=True)

        # Resample to 5-minute intervals
        df = df.resample('5T').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last',
                                    'volume': 'sum', 'quote_asset_volume': 'sum', 'number_of_trades': 'sum',
                                    'taker_buy_base_asset_volume': 'sum', 'taker_buy_quote_asset_volume': 'sum'})

        # Calculate 24-hour volume for each candle
        df['24h_volume'] = df['volume'].rolling(window=288).sum()

        # Calculate volume ratio for each candle starting from 289th row
        df['volume_ratio'] = 0.0
        df['sell_buy_ratio'] = 0.0
        df['order_type'] = ''
        for i in range(288, len(df)):
            volume = pd.to_numeric(df.iloc[i]['volume'])
            volume_24h = pd.to_numeric(df.iloc[i]['24h_volume'])
            if volume_24h > 0:
                volume_ratio = volume / volume_24h
                df.at[df.index[i], 'volume_ratio'] = volume_ratio

                # Calculate sell/buy ratio for each candle
                taker_buy_base_asset_volume = pd.to_numeric(df.iloc[i]['taker_buy_base_asset_volume'])
                taker_sell_base_asset_volume = pd.to_numeric(df.iloc[i]['volume']) - taker_buy_base_asset_volume
                if pd.isna(taker_sell_base_asset_volume):
                    taker_sell_base_asset_volume = 0
                order_type = 'buy' if taker_buy_base_asset_volume > taker_sell_base_asset_volume else 'sell'
                if volume > 0:
                    sell_buy_ratio = abs(taker_sell_base_asset_volume - taker_buy_base_asset_volume) / volume
                else:
                    sell_buy_ratio = 0

                df.at[df.index[i], 'sell_buy_ratio'] = sell_buy_ratio
                df.at[df.index[i], 'order_type'] = order_type

        # Filter for rows where volume ratio is greater than 0.02
        df_filtered = df[pd.to_numeric(df['volume_ratio']) > 0.06]
        date_list = []
        date_list.append("DATE")

        for index, row in df_filtered.iterrows():
            date = index.strftime("%Y-%m-%d %H:%M ")
            date_list.append(date)

        print(date_list)

        # Select relevant columns and rename them
        df_filtered = df_filtered[['volume', 'volume_ratio', 'sell_buy_ratio', 'order_type']]

        df_filtered2 = [list(df_filtered.columns)] + df_filtered.values.tolist()
        df_filtered2 = [[date] + row for date, row in zip(date_list, df_filtered2)]
        print(df_filtered2)
        return df_filtered2

def getConformeData(tab):
    list = []
    for i in range(len(tab)):
        if i==0:
            continue
        list.append( Alert(i,tab[i][0],tab[i][1],tab[i][2],tab[i][3],tab[i][4]))
    return list
def plot_data(tab):
    my_plots = []
    for item in tab :
        print("item in tab")
        print(item.Time)
        print(item.Numero)
        print(item.Price)
        print(item.VolumeChange)
        print(item.Up)
        print(item.Emoji)
        if item.Emoji =="sell":
         my_plots.append(-1 * item.VolumeChange/100)
        else:
         my_plots.append(-1 * item.VolumeChange/100)
    print(my_plots)
    return my_plots

def plot_date(tab):
    my_plots = []
    for item in tab :
        my_plots.append(item.Numero)
    print(my_plots)
    return my_plots
def plot_date2(tab):
    my_plots = []
    for item in tab :
        my_plots.append(item.Up)
    print(my_plots)
    return my_plots