from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    slug = forms.SlugField(required=False)
    class Meta:
        model = Book
        fields = '__all__'