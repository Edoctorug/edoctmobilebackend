"""
ASGI config for patientdoctor_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chatapp.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patientdoctor_chat.settings')

#application = get_asgi_application()
django_asgi = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi,
        "websocket": 
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ,
    }
)

