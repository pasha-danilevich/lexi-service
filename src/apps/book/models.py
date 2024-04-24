from django.db import models
from django.utils.text import slugify
from .utils import transliterate

class Book(models.Model):
    title = models.CharField('title', max_length=255, blank=False)
    author = models.CharField('author', max_length=255, blank=True)
    page_count = models.IntegerField('page_count', blank=False)
    slug = models.SlugField('slug', null=False, blank=False, unique=True)
    author_upload = models.ForeignKey(
        'user.User', 
        related_name='author_upload', 
        on_delete=models.SET_NULL, 
        null=True
        )
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        slug = f'{self.title}-{self.author}'
        self.slug = slugify(transliterate(slug))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        
        return reverse("books-retrieve", kwargs={"pk": self.pk})
    