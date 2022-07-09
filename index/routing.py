from django.urls import re_path
from . import consumers, CheckConsumers

websocket_urlpatterns = [
  re_path(r'^ws/notify/?$', consumers.NotifyConsumer.as_asgi()),
  re_path(r'^ws/check/?$', CheckConsumers.CheckConsumer.as_asgi()),
]