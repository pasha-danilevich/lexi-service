from django.urls import path
from apps.api.v1.user.api import BookmarkListCreate, UserActivate

urlpatterns = [
    path('bookmarks/', BookmarkListCreate.as_view(), name='bookmark-list'),
    path("activation/<str:uid>/<str:token>/", UserActivate.as_view({"post": "activation"}), name="activate")
] 