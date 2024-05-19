from django.urls import path
from rest_framework_simplejwt import views

urlpatterns = [
    path('create/', views.TokenObtainPairView.as_view(), name="jwt-create"),
    path('refresh/', views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path('verify/', views.TokenVerifyView.as_view(), name="jwt-verify"),
] 