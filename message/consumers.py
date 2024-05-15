import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


# Utilities like asgiref.sync.sync_to_async and channels.db.database_sync_to_async can be used
# to call synchronous code from asynchronous consumer
# performance gains however would be less than if it only used async-native libraries
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # joins a group
        # async_to_sync wrapper is required: chatconsumer is a synchronous websocket consumer
        # but is calling an asynchronous channel layer method (all channel layer methods are asynchronous)
        # group names are restricted to ASCII alphanumerics, hyphens and periods only (max 100 in default backend)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # accepts websocket connection
        # recommended that accept be last action in connect() if you want to accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        # leaves the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # sends an event to a group
        # event has special type key _> corresponding to the name of the method that should be invoked
        # on consumers that receive the event
        # translation is done by replacing . with _ thus chat.message -> chat_message
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat.message', "message": message})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
