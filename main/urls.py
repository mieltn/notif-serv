from django.urls import path
from .views import Clients, MailingLists

urlpatterns = [
    path('clients/', Clients.as_view()),
    path('clients/<int:id>', Clients.as_view()),
    path('mailinglists/', MailingLists.as_view()),
    path('mailinglists/<int:id>', MailingLists.as_view()),
]