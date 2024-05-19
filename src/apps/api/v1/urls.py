from django.urls import path, include


urlpatterns = [
    path('books/', include('apps.api.v1.book.urls')),
    path('users/', include('apps.api.v1.user.urls')),
    path('words/', include('apps.api.v1.word.urls')),
    path('vocabulary/', include('apps.api.v1.vocabulary.urls')),
    path('training/', include('apps.api.v1.training.urls')),
    path('jwt/', include('apps.api.v1.jwt.urls'))
] 