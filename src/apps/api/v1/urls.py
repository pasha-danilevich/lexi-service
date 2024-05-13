from django.urls import path, include

urlpatterns = [
    path('books/', include('apps.api.v1.book.urls')),
    path('users/', include('apps.api.v1.user.urls')),
    path('words/', include('apps.api.v1.word.urls')),
    path('vocabulary/', include('apps.api.v1.vocabulary.urls')),
] 