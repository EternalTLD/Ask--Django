import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from questions.routing import questions_websocket_urlpatterns
from notifications.routing import notifications_websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ask_project.settings')
django.setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    questions_websocket_urlpatterns +
                    notifications_websocket_urlpatterns
                )
            )
        ),
    }
)