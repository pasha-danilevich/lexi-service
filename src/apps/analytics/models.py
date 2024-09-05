from django.db import models


class CountPartOfSpeech(models.Model):
    date_create = models.DateTimeField("Date Created", auto_now_add=True)
    date_update = models.DateTimeField("Date Updated", auto_now=True)
    
    part_of_speech = models.ForeignKey(
        'word.PartOfSpeech',
        verbose_name="Part of Speech",
        related_name='count_part_of_speech',
        on_delete=models.CASCADE,
        null=True
    )
    
    count = models.PositiveIntegerField("Count")
    

    def __str__(self) -> str:
        return f"{self.part_of_speech.text} - {self.count}" # type: ignore