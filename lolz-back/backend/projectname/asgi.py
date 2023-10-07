import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from projectname import routing  # Replace with your actual Django app name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # This should now be recognized
        )
    ),
})
