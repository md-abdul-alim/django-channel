from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
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


class PizzaConsumer(WebsocketConsumer):
    
    def connect(self, **kwargs):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        order = Order.give_order_details(self.room_name)
        self.accept()

        self.send(text_data=json.dumps({
            "payload": order
        }))
    
    def order_status(self, event):
        print(event)
        data = json.loads(event['value'])
        print(data)

    def receive(self, text_data=None, bytes_data=None):
        print(type(text_data))

    def disconnect(self, code):
        print('Disconnected: ', code)
        pass