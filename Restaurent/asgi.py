"""
ASGI config for Restaurent project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from unittest.mock import AsyncMagicMixin
from django.core.asgi import get_asgi_application
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurent.settings')
django_asgi_app = get_asgi_application()

import Resto.routing
  
application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket":AuthMiddlewareStack( 
                    URLRouter(
                Resto.routing.websocket_urlpatterns
            )
        )
})
