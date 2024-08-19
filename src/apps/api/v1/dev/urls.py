from django.urls import path
from .api import PingView

urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
] 