from django.urls import path , include
from Trade.consumers import ChatConsumer,Chat2Consumer,Chat3Consumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
	path("ws/_consumers_xcv/" , ChatConsumer.as_asgi()) ,
	path("ws/consumers2_kfb/" , Chat2Consumer.as_asgi()) ,
	path("ws/consumers3_zjb/" , Chat3Consumer.as_asgi()) ,

]
