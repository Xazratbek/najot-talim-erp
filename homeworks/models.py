from django.db import models
from common.models import TimeStampedModel
from groups.models import GroupLesson
from users.models import User


class Homework(TimeStampedModel):
    group_lesson = models.ForeignKey(
        GroupLesson,
        on_delete=models.CASCADE,
        related_name='homeworks'
    )

    file = models.FileField(upload_to='homeworks/')
    description = models.TextField()
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = "Uyga vazifa"
        verbose_name_plural = "Uyga vazifalar"
        ordering = ['-id']

    def __str__(self):
        return self.title


class HomeworkSubmission(TimeStampedModel):

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='homeworks/submissions/'
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Uyga vazifa topshirig'i"
        verbose_name_plural = "Uyga vazifa topshiriqlari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.homework}"