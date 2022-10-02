from django.urls import path
from .views import Clients, MailingLists, DetailedStat, GeneralStat

urlpatterns = [
    path('clients/', Clients.as_view(), name='clients'),
    path('clients/<int:id>', Clients.as_view(), name='client'),
    path('mailinglists/', MailingLists.as_view(), name='mailinglists'),
    path('mailinglists/<int:id>', MailingLists.as_view(), name='mailinglist'),
    path('generalstat/', GeneralStat.as_view(), name='generalstat'),
    path('detailedstat/<int:id>', DetailedStat.as_view(), name='detailedstat'),
]