from django.db import models
# from apps.user.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField('title', max_length=255, blank=False)
    author = models.CharField('author', max_length=255, blank=False)
    page_count = models.IntegerField('page count', blank=False)
    author_upload = models.ForeignKey(
        'user.User', 
        related_name='author_upload', 
        on_delete=models.SET_NULL, 
        null=True
        )
    
    def __str__(self) -> str:
        return self.title