from django.urls import path
from .api import RecentlyWord, VocabularyStats

urlpatterns = [
    path('vocabulary/', VocabularyStats.as_view(), name='vocabulary-stat'),
    path('recently-words/', RecentlyWord.as_view(), name='recently-words-stat'),
] 