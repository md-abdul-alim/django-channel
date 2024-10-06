from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
import json
from .models import Order, Pizza

class MainConsumer(WebsocketConsumer):
    
    def connect(self, **kwargs):
        self.room_name = 'main_room'
        self.group_name = 'main_room'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'message': "connection made"
        }))

    def receive(self, text_data=None, bytes_data=None):
        print(type(text_data))

    def disconnect(self, code):
        print('Disconnected: ', code)
        pass


# class PizzaConsumerSync(WebsocketConsumer):
    
#     def connect(self, **kwargs):
#         self.room_name = self.scope['url_route']['kwargs']['order_id']
#         self.room_group_name = f'order_{self.room_name}'

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         order = Order.give_order_details(self.room_name)
#         self.accept()

#         self.send(text_data=json.dumps({
#             "payload": order
#         }))
    
#     def sync_order_status(self, event):
#         data = json.loads(event['value'])

#         self.send(text_data=json.dumps({
#             "payload": data
#         }))

#     def receive(self, text_data=None, bytes_data=None):
#         print(type(text_data))

#     def disconnect(self, code):
#         print('Disconnected: ', code)
#         # Leave the group
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )


class PizzaConsumerAsync(AsyncWebsocketConsumer):
    
    async def connect(self, **kwargs):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}'

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Fetch order details asynchronously
        order = await sync_to_async(Order.give_order_details)(self.room_name)

        # Accept the WebSocket connection
        await self.accept()

        # Send order details
        await self.send(text_data=json.dumps({
            "message": 'Connected successfully',
            "payload": order
        }))
    
    async def async_order_status(self, event):
        data = json.loads(event['value'])

        # Send updated status to WebSocket
        await self.send(text_data=json.dumps({
            "payload": data
        }))

    async def receive(self, text_data=None, bytes_data=None):
        print(type(text_data))

    async def disconnect(self, code):
        print('Disconnected: ', code)
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )