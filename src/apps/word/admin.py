from django.contrib import admin
from apps.word.models import Word, UserWordRelation
# Register your models here.


admin.site.register(Word)
admin.site.register(UserWordRelation)