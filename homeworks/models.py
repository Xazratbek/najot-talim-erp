from django.db import models
from common.models import TimeStampedModel
from groups.models import GroupLesson
from users.models import User
from django.db.models import Q, Count


class HomeWorkStatusChoices(models.TextChoices):
    WAITING = "waiting", "Kutayotganlar"
    NOT_SUBMITTED = "not_submitted", "Bajarilmagan"
    REJECTED = "rejected", "Qaytarilgan"
    APPROVED = "approved", "Qabul qilingan"


class Homework(TimeStampedModel):
    group_lesson = models.ForeignKey(
        GroupLesson,
        on_delete=models.CASCADE,
        related_name='homeworks'
    )
    description = models.TextField()
    deadline = models.DateTimeField()
    video_file = models.FileField(upload_to='homeworks/videos/', blank=True, null=True)

    class Meta:
        db_table = 'homeworks'
        verbose_name = "Uyga vazifa"
        verbose_name_plural = "Uyga vazifalar"
        ordering = ['-id']

    def __str__(self):
        return self.description

    def get_submission_stats(self):
        stats = self.submissions.aggregate(
            topshirganlar=Count('id', filter=Q(status=HomeWorkStatusChoices.WAITING)),
            topshirmaganlar=Count('id', filter=Q(status=HomeWorkStatusChoices.NOT_SUBMITTED)),
            tekshirilganlar=Count('id', filter=Q(status=HomeWorkStatusChoices.APPROVED)),
        )
        return stats


class HomeworkFiles(TimeStampedModel):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='homework_files')
    file = models.FileField(upload_to='homeworks/materials/')

    class Meta:
        db_table = 'homework_files'


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
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=25,
        choices=HomeWorkStatusChoices.choices,
        default=HomeWorkStatusChoices.NOT_SUBMITTED,
        db_index=True,
    )
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    teacher_comment = models.TextField(blank=True, verbose_name="O'qituvchi izohi")
    checked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="checked_homework_submissions",
    )
    checked_at = models.DateTimeField(null=True, blank=True)
    allow_resubmission = models.BooleanField(default=False)

    class Meta:
        db_table = 'homework_submissions'
        verbose_name = "Uyga vazifa topshirig'i"
        verbose_name_plural = "Uyga vazifa topshiriqlari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.homework}"


class HomeworkSubmissionFiles(TimeStampedModel):
    homework_submission = models.ForeignKey(HomeworkSubmission, on_delete=models.CASCADE, related_name='homeworksubmission_files')
    file = models.FileField(upload_to='homeworks/submissions/')

    class Meta:
        db_table = 'homeworksubmission_files'
