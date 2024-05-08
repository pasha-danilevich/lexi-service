from django.urls import path
from apps.api.v1.user.api import BookmarkListCreate, BookmarkDestroy, UserActivate

urlpatterns = [
    path('bookmarks/', BookmarkListCreate.as_view(), name='bookmark-list'),
    path('bookmarks/<int:pk>', BookmarkDestroy.as_view(), name='bookmark-delete'),
    path("activation/<str:uid>/<str:token>/", UserActivate.as_view({"post": "activation"}), name="activate")
] 