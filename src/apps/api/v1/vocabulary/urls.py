from django.urls import path
from .api import VocabularyListCreate, VocabularyStats


urlpatterns = [
    path('', VocabularyListCreate.as_view(), name='vocabulary-list-create'),
    path('stats/', VocabularyStats.as_view(), name='vocabulary-stats'),
] 