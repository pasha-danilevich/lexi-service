from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import BookmarkViewSet

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]