from django.contrib import admin
from .models import Book
from .forms import BookForm

class BookAdmin(admin.ModelAdmin):
    form = BookForm

admin.site.register(Book, BookAdmin)