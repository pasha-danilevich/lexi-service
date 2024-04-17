from django.urls import path, include

urlpatterns = [
    path('books/', include('apps.api.v1.book.urls')),
    # path('words/', include('apps.api.v1.word.urls'))
] 