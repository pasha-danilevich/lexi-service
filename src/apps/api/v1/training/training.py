
from apps.user.models import User
from django.db.models.query import QuerySet
from apps.word.utils import get_current_unix_time

class Training:
    def __init__(self, queryset: QuerySet, user: User) -> None:
        self.queryset = queryset
        self.user = user
        
    def _get_item(self):
        ...
    
    def get_queryset(self):
        return self.queryset.filter(user=self.user)
    
    def get_queryset_to_training(self):
        count_word_in_round = self.user.settings.count_word_in_round
        training_queryset = self.get_queryset()
        return training_queryset.filter(time_lte=get_current_unix_time())[:count_word_in_round]   
    
    def raise_level(self):
        ...
    def reduce_level(self):
        ...
        
    def delete(self):
        ...
        
    def freeze(self):
        ...
    
class Recognize(Training):
    def get_list(self):
        ...
    
class Reproduce(Training):
    ...
    
class Puzzel(Training):
    ...
    
class Sprint(Training):
    ...