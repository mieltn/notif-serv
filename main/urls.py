from django.urls import path
from .views import Clients

urlpatterns = [
    path("clients/", Clients.as_view(), name="clients"),
]