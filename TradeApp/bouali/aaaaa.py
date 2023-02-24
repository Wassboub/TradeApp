import pandas as pd
import numpy as np

import dateparser
import pytz
import json

import datetime as dt
from datetime import datetime, timedelta
import time

from tqdm import tqdm as tqdm

import os
import joblib
import operator
from termcolor import colored

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager

from pricechange import *
from binanceHelper import *
from pricegroup import *

import telebot

import json
import requests
import redis
import websocket
import random,time
#round(message["rpc"],3)


def main():
   
        print('started')

        ws = websocket.WebSocket()
        ws.connect('ws://127.0.0.1:8000/ws/_consumers_xcv/')

        Dictionary ={'s': 'AUDUSDT', 'tvc': round(0.9204210570055297,5), 'c': 1, 't': '02/08/2023  21:23', 'v': 12435164.0, 'lp': 0.6961, 'tpc': round(0.08612028132624285,5), 'rpc': round(-0.08612028132624285,5)}                          

        for i in range(40):
            print("i a pour valeur", i)        
            ws.send(json.dumps({'message' : Dictionary ,  'username' : 'binance' }))
            time.sleep(5)

       
    
        return


if __name__ == '__main__':
    main()
