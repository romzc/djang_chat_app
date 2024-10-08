"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chats import consumers
from chats.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from core.middlewares import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter({
   "http": get_asgi_application(),
   "websocket": JWTAuthMiddlewareStack(
      URLRouter(websocket_urlpatterns)
   ),
})