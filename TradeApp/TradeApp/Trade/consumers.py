import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Trade.models import CoinInfo,CoinInfo_2
from channels.db import database_sync_to_async
from datetime import datetime, timedelta


class ChatConsumer(AsyncWebsocketConsumer):

	@database_sync_to_async
	def create_coinsInfo(self,message):
		coinInfo = CoinInfo()
		coinInfo.symbol = message["s"]
		coinInfo.Time = datetime.strptime(message["t"], '%d/%m/%Y %H:%M')
		coinInfo.Ticks = message["c"]
		coinInfo.RelativePriceChange = round(message["rpc"],3)
		coinInfo.TotalPriceChange = round(message["tpc"],3)
		coinInfo.VolumeChange = round(message["tvc"],3)
		coinInfo.LastPrice = round(message["lp"],3)
		coinInfo.LastVolume = round(message["v"],3)
		return coinInfo.save()

	async def connect(self):
		self.roomGroupName = "group_chat_gfg"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName ,
			self.channel_name
		)
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		print('chat 1')
		if(username == "binance"):
			await self.create_coinsInfo(message)
			#twohours = datetime.now() + timedelta(hours=2)
			message["t"] = datetime.now().strftime('%d/%m/%Y %H:%M')
			await self.channel_layer.group_send(
				self.roomGroupName,{
					"type" : "sendMessage" ,
					"message" : message ,
					"username" : username ,
				})
		

	async def sendMessage(self , event) :
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message}))

	def getCoinInfo(data):
		coinInfo =  CoinInfo()
		message = json.loads(data)
		coinInfo.symbol = message["s"]
		coinInfo.symbol = message["t"]
		coinInfo.symbol = message["c"]
		coinInfo.symbol = message["rpc"]
		coinInfo.symbol = message["tpc"]
		coinInfo.symbol = message["tvc"]
		coinInfo.symbol = message["lp"]
		coinInfo.symbol = message["v"]
		return coinInfo


class Chat2Consumer(AsyncWebsocketConsumer):

	@database_sync_to_async
	def create_coinsInfo(self,message):
		coinInfo_2 = CoinInfo_2()
		coinInfo_2.symbol = message["s"]
		coinInfo_2.Time = datetime.strptime(message["t"], '%d/%m/%Y %H:%M')
		coinInfo_2.Ticks = message["c"]
		coinInfo_2.RelativePriceChange = round(message["rpc"],3)
		coinInfo_2.TotalPriceChange = round(message["tpc"],3)
		coinInfo_2.VolumeChange = round(message["tvc"],3)
		coinInfo_2.LastPrice = round(message["lp"],3)
		coinInfo_2.LastVolume = round(message["v"],3)
		return coinInfo_2.save()

	async def connect(self):
		self.roomGroupName = "group_chat_gfg_2"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName ,
			self.channel_name
		)
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		print('chat 2')
		if(username == "binance"):
			await self.create_coinsInfo(message)
			await self.channel_layer.group_send(
				self.roomGroupName,{
					"type" : "sendMessage" ,
					"message" : message ,
					"username" : username ,
				})
		

	async def sendMessage(self , event) :
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message}))

	def getCoinInfo(data):
		coinInfo_2 =  CoinInfo()
		message = json.loads(data)
		coinInfo_2.symbol = message["s"]
		coinInfo_2.symbol = message["t"]
		coinInfo_2.symbol = message["c"]
		coinInfo_2.symbol = message["rpc"]
		coinInfo_2.symbol = message["tpc"]
		coinInfo_2.symbol = message["tvc"]
		coinInfo_2.symbol = message["lp"]
		coinInfo_2.symbol = message["v"]
		return coinInfo_2


class Chat3Consumer(AsyncWebsocketConsumer):

	@database_sync_to_async
	def create_coinsInfo(self,message):
		coinInfo_2 = CoinInfo_2()
		coinInfo_2.symbol = message["s"]
		coinInfo_2.Time = datetime.strptime(message["t"], '%d/%m/%Y %H:%M')
		coinInfo_2.Ticks = message["c"]
		coinInfo_2.RelativePriceChange = round(message["rpc"],3)
		coinInfo_2.TotalPriceChange = round(message["tpc"],3)
		coinInfo_2.VolumeChange = round(message["tvc"],3)
		coinInfo_2.LastPrice = round(message["lp"],3)
		coinInfo_2.LastVolume = round(message["v"],3)
		return coinInfo_2.save()

	async def connect(self):
		self.roomGroupName = "group_chat_gfg_3"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName ,
			self.channel_name
		)
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		print('chat 3')
		if(username == "binance"):
			await self.create_coinsInfo(message)
			await self.channel_layer.group_send(
				self.roomGroupName,{
					"type" : "sendMessage" ,
					"message" : message ,
					"username" : username ,
				})
		

	async def sendMessage(self , event) :
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message}))

	def getCoinInfo(data):
		coinInfo_2 =  CoinInfo()
		message = json.loads(data)
		coinInfo_2.symbol = message["s"]
		coinInfo_2.symbol = message["t"]
		coinInfo_2.symbol = message["c"]
		coinInfo_2.symbol = message["rpc"]
		coinInfo_2.symbol = message["tpc"]
		coinInfo_2.symbol = message["tvc"]
		coinInfo_2.symbol = message["lp"]
		coinInfo_2.symbol = message["v"]
		return coinInfo_2
