from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('apps.api.v1.urls')), # current version
    # path('v0/', include('apps.api.v0.urls')) example of versioning
] 