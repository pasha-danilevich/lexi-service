from django.urls import path
from .api import BookListCreate, BookRetrieve, BookmarkListCreate, BookmarkDeleteView, OwnBookList

urlpatterns = [
    path('', BookListCreate.as_view(), name='book-list-create'),
    path('<slug:slug>/<int:page>', BookRetrieve.as_view(), name='books-retrieve'), # details
    
    path('my/', OwnBookList.as_view()),
    
    path('bookmarks/', BookmarkListCreate.as_view(), name='bookmark-list-create'),
    path('bookmarks/<int:pk>/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
]