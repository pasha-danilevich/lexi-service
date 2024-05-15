from typing import Iterable
from django.db import models
from .utils import get_current_unix_time




class Word(models.Model):
    text = models.CharField(max_length=100)
    part_of_speech = models.CharField(max_length=100, null=True, blank=True)  # Часть речи
    transcription = models.CharField(max_length=100, null=True, blank=True)  # Транскрипция

    def __str__(self):
        return self.text


class Translation(models.Model):
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name='translations')
    text = models.CharField(max_length=100)
    part_of_speech = models.CharField(max_length=100, null=True, blank=True)  # Часть речи
    gender = models.CharField(max_length=2, null=True, blank=True)  # Род
    frequency = models.IntegerField(null=True, blank=True)  # Частота использования

    def __str__(self):
        return self.text


class Synonym(models.Model):
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name='synonyms')
    text = models.CharField(max_length=100)
    part_of_speech = models.CharField(max_length=100, null=True, blank=True)  # Часть речи
    gender = models.CharField(max_length=2, null=True, blank=True)  # Род
    frequency = models.IntegerField(null=True, blank=True)  # Частота использования

    def __str__(self):
        return self.text


class Meaning(models.Model):
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name='meanings')
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


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
