"""
WSGI config for patientdoctor_chat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os,django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patientdoctor_chat.settings')
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chatapp.routing import websocket_urlpatterns

dapplication = get_wsgi_application()
application = ProtocolTypeRouter(
    {
        "http": dapplication,
        "websocket": 
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ,
    }
)
app = application