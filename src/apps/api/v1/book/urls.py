from django.urls import path
from .api import BookViewSet

urlpatterns = [
    path('', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list-create'),
    path('<slug:slug>/<int:page>/', BookViewSet.as_view({'get': 'retrieve'}), name='book-retrieve'),
    path('my/', BookViewSet.as_view({'get': 'list_own_books'}), name='own-book-list'),
    path('my/<slug:slug>/', BookViewSet.as_view({'delete': 'destroy'}), name='own-book-delete'),
]