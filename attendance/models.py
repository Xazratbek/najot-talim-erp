from django.db import models
from groups.models import GroupLesson
from users.models import User
from common.models import TimeStampedModel

class Status(models.TextChoices):
    PRESENT = "present", "Keldi"
    ABSENT = "absent", "Kelmadi"

class Attendance(TimeStampedModel):
    group_lesson = models.ForeignKey(
        GroupLesson,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        db_index=True,
    )

    class Meta:
        verbose_name = "Yo'qlama"
        verbose_name_plural = "Yo'qlamalar"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.status}"