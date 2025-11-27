import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psiconfig.settings')

# Primeiro inicializa o Django
django_asgi_app = get_asgi_application()

# SÓ DEPOIS pode importar routing, porque agora as apps já carregaram
import psiconnect.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            psiconnect.routing.websocket_urlpatterns
        )
    ),
})
