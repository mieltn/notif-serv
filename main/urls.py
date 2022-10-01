from django.urls import path
from .views import Clients, MailingLists, DetailedStat, GeneralStat

urlpatterns = [
    path('clients/', Clients.as_view()),
    path('clients/<int:id>', Clients.as_view()),
    path('mailinglists/', MailingLists.as_view()),
    path('mailinglists/<int:id>', MailingLists.as_view()),
    path('generalstat/', GeneralStat.as_view()),
    path('detailedstat/<int:id>', DetailedStat.as_view()),
]