from django.db import models
from common.models import TimeStampedModel
from groups.models import Group
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
class Exam(TimeStampedModel):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='exams',
        db_index=True
    )
    title = models.CharField(max_length=255,db_index=True)
    description = models.TextField()
    started_at = models.DateTimeField(db_index=True)
    ended_at = models.DateTimeField()
    allow_resubmission = models.BooleanField(default=False)

    class Meta:
        db_table = 'exams'
        verbose_name = "Imtihon"
        verbose_name_plural = "Imtihonlar"
        ordering = ['-id']

    def __str__(self):
        return self.title


class ExamSubmission(TimeStampedModel):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
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
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],default=0)

    class Meta:
        db_table = 'exam_submissions'
        verbose_name = "Imtihon topshirig'i"
        verbose_name_plural = "Imtihon topshiriqlari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.exam}"

class ExamsubmissionFiles(TimeStampedModel):
    exam_submission = models.ForeignKey(ExamSubmission,on_delete=models.CASCADE,related_name='files')
    file = models.FileField(
        upload_to='exams/submissions/'
    )

    class Meta:
        db_table = 'examsubmission_files'