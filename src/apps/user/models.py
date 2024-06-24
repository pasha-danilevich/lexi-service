from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser

# Create your models here.
from apps.book.models import Book


# from django.core.mail import send_mail
# from users_app.managers import UserManager
def settings_default():
    data = {
        "dark_theme": False,
        "levels": [1, 3, 5, 7, 11],
        "number_of_false_set": 4,
        "count_word_in_round": 10
    }
    return data


class User(AbstractUser):
    first_name = None
    last_name = None

    is_active = models.BooleanField("active", default=True)
    activated_email = models.BooleanField("activated_email", default=False)
    email = models.EmailField("email address", blank=False, unique=True)
    settings = models.JSONField(default=settings_default, null=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        unique_together = ('username', 'email',)


class UserBookRelation(models.Model):
    user = models.ForeignKey(
        User, related_name='related_books', on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='related_users', on_delete=models.CASCADE)
    target_page = models.IntegerField('target page', blank=False)

    def __str__(self) -> str:
        return f"User: {self.user} left a bookmark {self.target_page}. Book: {self.book} "
