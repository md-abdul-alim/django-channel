pip install django
pip install channels[daphne]
pip install channels-redis

=> Now go to django settings installed app & add ``'daphne'``
=> Add path of channel redis broker path in setting: ``https://github.com/django/channels_redis?tab=readme-ov-file#usage``

'''
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
'''
=> Now update application path: ``WSGI_APPLICATION = 'realtime.wsgi.application'`` to ``ASGI_APPLICATION = 'realtime.asgi.application'``


# now update asgi.py routing: https://channels.readthedocs.io/en/latest/topics/routing.html

=> configure asgi.py routing


# now create the consumer: https://channels.readthedocs.io/en/latest/topics/consumers.html#websocketconsumer
=> create consumers.py

# concept of room
    -> private room: if i have to send message to specific user
    -> public / broadcast room: if i have to sent the message to multiple user


# for testing websocket request use websocket king: https://websocketking.com/
=> Test url by like: ws://localhost:8000/ws/main/