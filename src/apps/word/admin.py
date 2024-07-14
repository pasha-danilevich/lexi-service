from django.contrib import admin
from apps.word.models import *
# Register your models here.


admin.site.register(Word)
admin.site.register(Translation)
admin.site.register(Synonym)
admin.site.register(Meaning)
admin.site.register(Dictionary)
admin.site.register(Training)
admin.site.register(TrainingType)
