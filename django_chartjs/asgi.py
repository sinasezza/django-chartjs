import os

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import re_path
from dashboard.consumers import DashboardConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chartjs.settings')


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r'ws/dashboard/$', DashboardConsumer.as_asgi()),
                ]
            )
        )
    ),
})