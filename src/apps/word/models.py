from django.db import models

# Create your models here.

PART_OF_SPEECH = {
    "noun": "существительное",
    "verb": "глагол",
    "adjective": "прилагательное",
    "adverb": "наречие",
    "preposition": "предлог",
    "conjunction": "союз",
    "interjection": "междометие"
}
TRIANING_TYPE = {
    "RC": "recognize",
    "RP": "reproduction "
}

class Word(models.Model):
    text = models.CharField("text", max_length=50, blank=False)
    part = models.CharField(
        "part", 
        max_length=12, 
        choices=PART_OF_SPEECH, 
        blank=True
        )
    transcription = models.CharField("transcription", max_length=50, blank=True)
    translation = models.CharField("translation", max_length=50, blank=False)
    
    def __str__(self) -> str:
        return f'{self.text} - {self.translation}'
    
class UserWordRelation(models.Model):
    time = models.IntegerField("time", blank=False)
    lvl = models.IntegerField("lvl", blank=False, default=1)
    type = models.CharField(
        "training type", 
        max_length=2,
        blank=False, 
        choices=TRIANING_TYPE,
        default="RC")
    user = models.ForeignKey("user.User", related_name='word_related_with_user', on_delete=models.CASCADE)
    word = models.ForeignKey("word.Word", related_name='user_related_with_word', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"User: {self.user} add {self.word}"
