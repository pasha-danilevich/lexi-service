from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser

# Create your models here.
from apps.book.models import Book


# from django.core.mail import send_mail
# from users_app.managers import UserManager
def settings_default():
    data = {
        "dark-theme": False,
        "levels": [1, 3, 5, 7, 11]
    }
    return data


class User(AbstractUser):
    first_name = None
    last_name = None
    
    is_active = models.BooleanField("active", default=False)
    email = models.EmailField("email address", blank=False, unique=True)
    settings = models.JSONField(default=settings_default, null=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    # objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        unique_together = ('username', 'email')
        
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

class UserBookRelation(models.Model):
    user = models.ForeignKey(User, related_name='book_related_with_user', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='users_related_with_book', on_delete=models.CASCADE)
    target_page = models.IntegerField('target page', blank=False)
    
    def __str__(self) -> str:
        return f"User: {self.user} left a bookmark {self.target_page}. Book: {self.book} "

    
# Чтобы добавить поле settings в модель User и хранить в нем 
# данные в формате JSON, вы можете использовать поле `JSONField` 
# из пакета `django.contrib.postgres.fields`.

# Вам нужно установить этот пакет, если вы его еще не установили:
# ```
# pip install django-jsonfield
# ```
# Затем, в своей модели User добавьте поле `settings` с типом `JSONField`:
# ```p ython
# from django.contrib.postgres.fields import JSONField

# class User(models.Model):
#     ...
#     settings = JSONField(default=dict)
# ```
# Теперь вы можете сохранять в этом поле данные в формате JSON:
# ```python
# user = User.objects.get(id=1)
# user.settings = {
#     "dark-theme": False,
#     "levels": [1, 3, 5, 10, 12]
# }
# user.save()
# ```
# Или использовать его в сериализаторе:
# ```python
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'settings']

#     settings = serializers.JSONField()
# ```
# Обратите внимание, что JSONField доступен только в PostgreSQL. 
# Если вы используете другую СУБД, вы можете использовать поле `TextField` и 
# сериализатор `JSONField` для сохранения и извлечения данных в формате JSON.

