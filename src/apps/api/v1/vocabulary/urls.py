from django.urls import path
from .api import VocabularyListCreate, VocabularyStats, VocabularyDelete


urlpatterns = [
    path('', VocabularyListCreate.as_view(), name='vocabulary-list-create'),
    path('delete/', VocabularyDelete.as_view(), name='vocabulary-delete'),
    path('stats/', VocabularyStats.as_view(), name='vocabulary-stats'),
] 