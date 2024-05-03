from django.urls import path
from apps.api.v1.book.api import BookListCreate, BookRetrieve

urlpatterns = [
    path('', BookListCreate.as_view(), name='books-list'),
    path('<slug:slug>/', BookRetrieve.as_view(), name='books-retrieve'), # details
] 