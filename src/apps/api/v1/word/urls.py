from django.urls import path
from apps.api.v1.word.api import WordCreate

urlpatterns = [
    path('', WordCreate.as_view(), name='word-create'),
    
] 