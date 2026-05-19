from django.db import models
from common.models import TimeStampedModel
from groups.models import GroupLesson
from users.models import User

class HomeWorkStatusChoices(models.TextChoices):
    WAITING = "waiting","Kutayotganlar"
    NOT_SUBMITTED = "not_submitted", "Bajarilmagan"
    REJECTED = "rejected", "Qaytarilgan"
    APPROVED = "approved", "Qabul qilingan"

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
        db_table = 'homeworks'
        verbose_name = "Uyga vazifa"
        verbose_name_plural = "Uyga vazifalar"
        ordering = ['-id']

    def __str__(self):
        return self.description


class HomeworkSubmission(TimeStampedModel):
    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )
    file = models.FileField(
        upload_to='homeworks/submissions/'
    )
    description = models.TextField(
        blank=True
    )
    status = models.CharField(max_length=25,choices=HomeWorkStatusChoices.choices,default=HomeWorkStatusChoices.NOT_SUBMITTED,db_index=True)

    class Meta:
        db_table = 'homework_submissions'
        verbose_name = "Uyga vazifa topshirig'i"
        verbose_name_plural = "Uyga vazifa topshiriqlari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.homework}"