from django.urls import path
from apps.api.v1.word.api import WordCreate, googletrans, dictionaryapi

urlpatterns = [
    path('', WordCreate.as_view(), name='word-create'),
    path('<int:pk>/', WordCreate.as_view(), name='word-get'),
    path('googletrans/', googletrans, name='googletrans'),
    path('dictionaryapi/', dictionaryapi, name='dictionaryapi'),
] 