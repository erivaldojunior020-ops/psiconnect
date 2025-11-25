import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import psiconnect.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psiconfig.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            psiconnect.routing.websocket_urlpatterns
        )
    ),
})
