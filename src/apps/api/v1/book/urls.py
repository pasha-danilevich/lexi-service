from django.urls import path
from apps.api.v1.book.api import BookList

urlpatterns = [
    path('', BookList.as_view(), name='books-list'),
    # path('<int:id>', ), # details
] 