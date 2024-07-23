from datetime import datetime, timedelta
from django.db import models

class DictionaryQuerySet(models.QuerySet):
    def all(self, user_id: int):
        if not user_id:
            return self.filter()
        return self.filter(user_id=user_id)
    
    def get_new_words_today(self):
        """
        Возвращает:
            QuerySet: Queryset новых слов, добавленных сегодня.
        """
        today = datetime.now().date()
        beginning_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = beginning_of_day + timedelta(days=1)
        
        return self.filter(
            **{'date_added__gte': beginning_of_day, 'date_added__lt': end_of_day}
        )

class DictionaryCustomManager(models.Manager):
    def get_queryset(self):
        return DictionaryQuerySet(self.model, using=self._db)
    
    def all(self, user_id):
        return self.get_queryset().all(user_id)
    
    def get_new_words_today(self):
        return self.get_queryset().get_new_words_today()
    
    