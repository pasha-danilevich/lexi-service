from django.urls import path
from .api import BookListCreate, BookRetrieve, BookmarkListCreate, BookmarkDestroy

urlpatterns = [
    path('', BookListCreate.as_view(), name='book-list-create'),
    path('<slug:slug>/<int:page>', BookRetrieve.as_view(), name='books-retrieve'), # details
    
    path('bookmarks/', BookmarkListCreate.as_view(), name='bookmark-list-create'),
    path('bookmarks/<int:pk>', BookmarkDestroy.as_view(), name='bookmark-delete'),
] 