from django.contrib import admin
from apps.word.models import Word, UserWord
# Register your models here.


admin.site.register(Word)
admin.site.register(UserWord)