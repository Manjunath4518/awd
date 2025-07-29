from django.urls import path
from .views import *


urlpatterns = [
    path('send-email/',send_email,name='send_email')
]
