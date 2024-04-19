from django.urls import path
from apps.api.v1.user.api import BookmarkList, UserActivate

urlpatterns = [
    path('bookmarks/', BookmarkList.as_view(), name='bookmark-list'),
    path("activation/<str:uid>/<str:token>/", UserActivate.as_view({"post": "activation"}), name="activate")
] 