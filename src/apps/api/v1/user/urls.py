from django.urls import path
from apps.api.v1.user.api import RetrieveUser

urlpatterns = [
    path('<str:username>', RetrieveUser.as_view(), name='user-retrieve')
] 