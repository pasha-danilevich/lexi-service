from typing import cast
from django.db.models import Q, QuerySet


from rest_framework.request import Request


from apps.api.v1.book.api import BookListCreate, BookmarkListCreate, OwnBookList
from apps.api.v1.vocabulary.api import VocabularyListCreate
from apps.api.v1.vocabulary.serializers import DictionaryListSerializer
from apps.book.models import Bookmark


class BaseSearch(BookListCreate):

    def post(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(
        self, 
        filters: list, 
        search_params: str, 
        querysey: QuerySet
    ):

        # Если параметр поиска не задан, возвращаем все объекты
        if search_params.strip() == '':
            return querysey

        # Объединяем условия с помощью reduce
        from functools import reduce
        from operator import or_

        filtered_queryset = querysey.filter(reduce(or_, filters))
        print(filtered_queryset)
        return filtered_queryset
    
    def get_search_params(self):
        data: dict[str, str] = self.request.data  # type: ignore
        return data.get('value', '')
    
    def get_filters(self, search_params: str):
        filters = [
            Q(title__icontains=search_params),
            Q(author__icontains=search_params),
            Q(slug__icontains=search_params),
        ]
        return filters
    
    
class BookListSearch(BaseSearch, BookListCreate):
    permission_classes = []

    def get_queryset(self):
        queryset = BookListCreate.get_queryset(self) 
        search_params = self.get_search_params()
        filters = self.get_filters(search_params)
        return super().get_queryset(filters, search_params, queryset)

class MyBookListSearch(BaseSearch, OwnBookList):
    
    def get_queryset(self):
        queryset = OwnBookList.get_queryset(self) 

        search_params = self.get_search_params()
        filters = self.get_filters(search_params)

        return super().get_queryset(filters, search_params, queryset)


class BookmarkListSearch(BookmarkListCreate, BaseSearch):
    
    def get_filters(self, search_params: str):
        filters = [
            Q(book__title__icontains=search_params),
            Q(book__author__icontains=search_params),
            Q(book__slug__icontains=search_params),
        ]
        return filters
    
    def get_queryset(self):
        queryset = super().get_queryset()


        search_params = self.get_search_params()
        filters = self.get_filters(search_params)
        
        return BaseSearch().get_queryset(filters, search_params, queryset)
    
    def post(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class VocabularyListSearch(VocabularyListCreate, BaseSearch):

    def get_serializer_class(self):
        return DictionaryListSerializer
    
    def get_filters(self, search_params: str):
        filters = [
            Q(word__text__icontains=search_params),
            Q(translation__text__icontains=search_params),
            # Q(word__text__regex=rf'^{search_params}..$')
        ]
        return filters

    def get_queryset(self):
        queryset = super().get_queryset()
        search_params = self.get_search_params()
        filters = self.get_filters(search_params)
        
        return BaseSearch().get_queryset(filters, search_params, queryset)
    
    def post(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)