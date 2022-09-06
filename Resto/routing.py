from django.urls import re_path
from django.urls import path,include
  
from . import consumer
  
websocket_urlpatterns = [
    re_path(r'ws/sendOrder/', consumer.SendOrderToKitchen.as_asgi()),
    re_path(r'ws/makeRecette/', consumer.Recette.as_asgi()),
]