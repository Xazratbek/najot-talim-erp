from django.db import models

from groups.models import Group
from users.models import User

class Exam(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='exams'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    allow_resubmission = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Imtihon"
        verbose_name_plural = "Imtihonlar"
        ordering = ['-id']

    def __str__(self):
        return self.title


class ExamSubmission(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to='exams/submissions/'
    )
    description = models.TextField(
        blank=True
    )
    checked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checked_exam_submissions'
    )
    checked_at = models.DateTimeField(
        null=True,
        blank=True
    )
    class Meta:
        verbose_name = "Imtihon topshirig'i"
        verbose_name_plural = "Imtihon topshiriqlari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.exam}"