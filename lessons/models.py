from django.db import models
from common.models import TimeStampedModel

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=255)
    lesson_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ["-id"]

    def __str__(self):
        return self.title