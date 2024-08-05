from django.urls import path
from .api import *
from djoser.views import UserViewSet

urlpatterns = [
    path('settings/', SettingsPageView.as_view(), name='settings'),

    # email
    path('set_email/',
         UserActivate.as_view({"post": "set_email"}), name="set_email"),
    path("activation/<str:uid>/<str:token>/",
         UserActivate.as_view({"get": "activation"}), name="activate"),
    path("resend_activation/",
         UserActivate.as_view({"post": "resend_activation"}), name="resend_activation"),

    # password
    path("set_password/",
         UserViewSet.as_view({"post": "set_password"}), name="set_password"),
    path("reset_password/",
         UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path("reset_password_confirm/",
         UserViewSet.as_view({"post": "reset_password_confirm"}), name="reset_password_confirm"),

]
