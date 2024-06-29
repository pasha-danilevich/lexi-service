from django.contrib import admin
from .models import User, UserBookRelation, Settings



admin.site.register(User)
admin.site.register(UserBookRelation)
admin.site.register(Settings)
