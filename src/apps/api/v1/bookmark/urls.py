from django.urls import path
from .api import BookmarkListCreate, BookmarkDeleteView

urlpatterns = [
    path('', BookmarkListCreate.as_view(), name='bookmark-list-create'),
    path('<int:pk>/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
]