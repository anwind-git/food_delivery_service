from django.urls import path
from organization.views import ContactsHome

app_name = 'organization'

urlpatterns = [
    path('contacts/', ContactsHome.as_view(), name='contacts'),
]