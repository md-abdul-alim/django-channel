import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime.settings')

django_asgi_app = get_asgi_application()

from pizza import consumers

websocket_urlpatterns = [
    path("ws/main/", consumers.MainConsumer.as_asgi()),
            
]

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket pizza handler
    "websocket": (

            URLRouter(websocket_urlpatterns)
        
    ),
})
