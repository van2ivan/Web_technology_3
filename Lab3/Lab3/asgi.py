"""
ASGI config for Lab3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lab3.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from contactbook_api.routing import websocket_urlpatterns
from contactbook_api.middleware import JwtAuthMiddlewareStack


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": JwtAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
