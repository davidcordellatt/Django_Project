import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() + datetime.timedelta(days=30)

    def was_published_past(self):
        return timezone.now() <= self.pub_date <= timezone.now() - datetime.timedelta(days=2)

    def was_published_actual(self):
        return timezone.now() > self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        if self.choice_set.all().count() < 0:
            super().delete()
            raise Exception("The question should have at least two choices")

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

