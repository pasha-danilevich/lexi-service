from django.db import models
from django.utils.text import slugify

from .utils import transliterate

def book_default():
    return None

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
    book = models.JSONField(default=book_default, null=False)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        slug = f'{self.title}-{self.author}'
        self.slug = slugify(transliterate(slug))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        
        return reverse("books-retrieve", kwargs={"pk": self.pk})

class UserBook(models.Model):
    user = models.ForeignKey(
        "user.User", related_name='related_books', on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='related_users', on_delete=models.CASCADE)
    target_page = models.IntegerField('target page', blank=False)

    def __str__(self) -> str:
        return f"User: {self.user} left a bookmark {self.target_page}. Book: {self.book} "
