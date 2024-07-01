from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser

# Create your models here.
from apps.book.models import Book


# from django.core.mail import send_mail
# from users_app.managers import UserManager
def levels_default():
    return [1, 3, 5, 7, 11]





class User(AbstractUser):
    first_name = None
    last_name = None

    is_active = models.BooleanField("active", default=True)
    activated_email = models.BooleanField("activated_email", default=False)
    email = models.EmailField("email address", blank=False, unique=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        unique_together = ('username', 'email',)  


class Settings(models.Model):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Темная'),
        ('red', 'Красная'),
        ('green', 'Зеленая'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    levels = models.JSONField(default=levels_default, null=False)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    count_word_in_round = models.IntegerField(default=10, null=False)
    number_of_false_set = models.IntegerField(default=3, null=False)
    time_to_view_result = models.IntegerField(default=1000, null=False)

class UserBookRelation(models.Model):
    user = models.ForeignKey(
        User, related_name='related_books', on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='related_users', on_delete=models.CASCADE)
    target_page = models.IntegerField('target page', blank=False)

    def __str__(self) -> str:
        return f"User: {self.user} left a bookmark {self.target_page}. Book: {self.book} "

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_settings(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)

@receiver(post_save, sender= User)
def save_settings(sender, instance: User, **kwargs):
    instance.settings.save()