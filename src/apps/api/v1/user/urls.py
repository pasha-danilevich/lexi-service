from django.urls import path
from .api import *

urlpatterns = [
    path('settings/', SettingsPageView.as_view(), name='settings'),

    path('bookmarks/', BookmarkListCreate.as_view(), name='bookmark-list'),
    path('bookmarks/<int:pk>', BookmarkDestroy.as_view(), name='bookmark-delete'),

    path("activation/<str:uid>/<str:token>/",
         UserActivate.as_view({"post": "activation"}), name="activate"),
    path("resend_activation/",
         UserActivate.as_view({"post": "resend_activation"}), name="resend_activation")
]
