from django.contrib import admin
from apps.word.models import Word, Translation, Synonym, Meaning, UserWord
# Register your models here.


admin.site.register(Word)
admin.site.register(Translation)
admin.site.register(Synonym)
admin.site.register(Meaning)
admin.site.register(UserWord)
