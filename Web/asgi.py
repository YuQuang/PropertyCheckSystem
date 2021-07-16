"""
ASGI config for Web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
import django
from channels.auth import AuthMiddlewareStack
import index.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Web.settings')
django.setup()


application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            index.routing.websocket_urlpatterns
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})