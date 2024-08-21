from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.api.v1.bookmark.api import BookmarkViewSet
from apps.api.v1.book.api import BookViewSet
# from apps.api.v1.home.api import HomeViewSet
# from apps.api.v1.user.api import UserViewSet
# from apps.api.v1.word.api import WordViewSet
# from apps.api.v1.vocabulary.api import VocabularyViewSet
# from apps.api.v1.training.api import TrainingViewSet
# from apps.api.v1.jwt.api import JWTViewSet
# from apps.api.v1.search.api import SearchViewSet

router = SimpleRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

book_list_create = BookViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
book_retrieve = BookViewSet.as_view({
    'get': 'retrieve'
})

# router.register(r'home', HomeViewSet, basename='home')
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'words', WordViewSet, basename='word')
# router.register(r'vocabulary', VocabularyViewSet, basename='vocabulary')
# router.register(r'training', TrainingViewSet, basename='training')
# router.register(r'jwt', JWTViewSet, basename='jwt')
# router.register(r'search', SearchViewSet, basename='search')


urlpatterns = [
    path('', include(router.urls)),
    # home
    path('home/', include('apps.api.v1.home.urls')),
    
    # bookmark
    # path('books/', book_list_create, name='book-list-create'),
    
    # book
    path('books/', book_list_create, name='book-list-create'),
    path('books/<slug:slug>/<int:page>', book_retrieve, name='book-retrieve'),
    # path('my-books/', book_list_create, name='book-list-create'),
    
    path('users/', include('apps.api.v1.user.urls')),
    path('words/', include('apps.api.v1.word.urls')),
    path('vocabulary/', include('apps.api.v1.vocabulary.urls')),
    path('training/', include('apps.api.v1.training.urls')),
    path('jwt/', include('apps.api.v1.jwt.urls')),
    path('search/', include('apps.api.v1.search.urls')),
    
    
    path('dev/', include('apps.api.v1.dev.urls'))
] 