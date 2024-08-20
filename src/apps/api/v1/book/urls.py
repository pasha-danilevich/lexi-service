from django.urls import path
from .api import BookListCreate, BookRetrieve, OwnBookList, OwnBookDelete

urlpatterns = [
    path('', BookListCreate.as_view(), name='book-list-create'),
    path('<slug:slug>/<int:page>', BookRetrieve.as_view(), name='books-retrieve'), 
    
    path('my/', OwnBookList.as_view()),
    path('my/<int:pk>/', OwnBookDelete.as_view()), 
]