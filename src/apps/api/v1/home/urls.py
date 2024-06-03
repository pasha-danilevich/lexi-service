from django.urls import path
from .api import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
] 