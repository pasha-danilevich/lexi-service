from django.urls import path
from .api import *

urlpatterns = [
    path('books/', BookListSearch.as_view(), name='book-list-search'),
    path('books/my/', MyBookListSearch.as_view(), name='book-my-list-search'),
    path('bookmark/', BookmarkListSearch.as_view(), name='bookmark-list-search'),
]