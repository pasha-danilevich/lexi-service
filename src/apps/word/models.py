from typing import Iterable
from django.db import models
from .utils import get_current_unix_time


from config.settings import print_local_var


class Word(models.Model):
    text = models.CharField("text", max_length=50, blank=False, unique=True)
    part = models.CharField("part", max_length=50, blank=True)
    transcription = models.CharField(
        "transcription", max_length=50, blank=True)
    translation = models.CharField("translation", max_length=50, blank=False)
    synonym = models.JSONField("synonym", null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.text} - {self.translation}'


class UserWord(models.Model):
    user = models.ForeignKey("user.User", related_name='related_words',
                             on_delete=models.CASCADE, blank=False, null=False)
    word = models.ForeignKey("word.Word", related_name='related_users',
                             on_delete=models.CASCADE, blank=False, null=False)

    recognize_lvl = models.IntegerField("recognize_lvl", default=1, null=False)
    recognize_time = models.IntegerField(
        "recognize_time",
        null=False
    )

    reproduce_lvl = models.IntegerField("reproduce_lvl", default=1, null=False)
    reproduce_time = models.IntegerField(
        "reproduce_time",
        null=False
    )

    class Meta:
        unique_together = ('user', 'word',)

    def save(self, *args, **kwargs) -> None:
        current_time = get_current_unix_time()
        self.recognize_time = current_time
        self.reproduce_time = current_time
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"User: {self.user} add {self.word}"
