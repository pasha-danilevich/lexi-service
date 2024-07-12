from django.urls import path
from .api import *
from djoser.views import UserViewSet

urlpatterns = [
    path('settings/', SettingsPageView.as_view(), name='settings'),

    path('set_email/',
         UserActivate.as_view({"post": "set_email"}), name="set_email"),
    path("activation/<str:uid>/<str:token>/",
         UserActivate.as_view({"post": "activation"}), name="activate"),
    path("resend_activation/",
         UserActivate.as_view({"post": "resend_activation"}), name="resend_activation"),
    path("set_password/", 
         UserViewSet.as_view({"post": "set_password"}), name="resend_activation")

]
