import json

from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncConsumer
from django.contrib.sessions.backends.db import SessionStore
from importlib import import_module
from django.conf import settings
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from .WSRouter import ChatRouter
from .WSResponseModel import WSResponseMdl

class ChatConsumer(AsyncWebsocketConsumer):
    ws_router = None
    def loadPK(self):
        XSessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        s = XSessionStore(session_key="46b5xm2rv4az2vwaduiosofjz4ibg501")

        print(s["auth_man"])
        
    async def connect(self):
        
        await self.accept()
        
        chat_name = self.channel_name
        #auth_man = self.scope["auth_man"]
        
        
        #loadpk = sync_to_async(self.loadPK)
        
        #await loadpk()
        
        #session_data = SessionStore().decode('46b5xm2rv4az2vwaduiosofjz4ibg501')
        #print("connected to : ",chat_name)
        self.ws_router = ChatRouter(self.channel_name)
        
        #print("auth man is: ", session_data)

    async def disconnect(self, close_code):
        super().disconnect(close_code)
        print(self.scope["data"])
        delUser = sync_to_async(self.ws_router.delUser)#use sync_to_async to call the async delUser function asynchronously
        await delUser() #remove channel name and make user offline
        pass

    async def receive(self, text_data):
        """
        Handles the receipt of text data.

        Args:
            text_data (str): The text data received.

        Returns:
            None
        """
        print(text_data)
        self.scope["data"] = "hello_world"
        text_data_json = json.loads(text_data)
       # message = text_data_json["message"]
        
        router_reply = await self.ws_router.route(text_data_json,self)
        if router_reply != None:
            await self.send(text_data=router_reply)
    
    async def chat_message(self, event):
        """
        Handles the chat message event.

        Args:
            event (dict): The event dictionary containing chat message details.

        Returns:
            None
        """
        print("event : ",event)
        response_mdl = WSResponseMdl(200,"chat",event["text"],{"chat_uuid":event["uuid"]})

        chat_json = response_mdl.serial()
        await self.send(text_data=chat_json)

    async def raw_chat_message(self, event):
        """
        Handles the raw chat message event.

        Args:
            event (dict): The event dictionary containing raw chat message details.

        Returns:
            None
        """
        print("event : ",event)
        #response_mdl = WSResponseMdl(200,"chat",event["text"])

        #chat_json = response_mdl.serial()
        await self.send(text_data=event["text"])

class XChatConsumer(AsyncConsumer):
    async def websocket_connect(self):
        self.accept()
        chat_name = self.channel_name

        print("connected to : ",chat_name)

    async def websocket_disconnect(self, close_code):
        pass

    async def websocket_receive(self, text_data):
        """
        Handles the receipt of text data for a WebSocket connection.

        Args:
            text_data (str): The text data received.

        Returns:
            None
        """
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))