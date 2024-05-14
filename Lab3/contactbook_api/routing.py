from django.urls import re_path
from .consumers import ContactConsumer, NotifyAdminConsumer

websocket_urlpatterns = [
    re_path("ws/contact/", ContactConsumer.as_asgi()),
    re_path("ws/notify/", NotifyAdminConsumer.as_asgi())
]