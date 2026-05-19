from users.models import User
from django.db import models
from common.models import TimeStampedModel

class NotificationTypes(models.TextChoices):
    NEW_EXAM = "new_exam", "Yangi imtihon"
    NEW_LESSON = "new_lesson","Yangi dars"
    EXAM_ANNOUNCEMENT = "exam_announcement", "Imtihon e'loni"
    XP_UPDATE = "xp_update", "XP yangilanishi"
    EXAM_DEADLINE_NEAR = "exam_deadline_near", "Imtihon muddati yaqin"
    HOMEWORK_REVIEWED = "homework_reviewed", "Uyga vazifa tekshirildi"
    ADDED_TO_GROUP = "added_to_group", "Guruhga qo'shildingiz"
    REMOVED_FROM_GROUP = "removed_from_group", "Guruhdagi o'qish to'xtatildi"
    SILVER_REWARDED = "silver_rewarded", "XP/Kumush berildi"


class Notification(TimeStampedModel):
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Qabul qiluvchi"
    )
    type = models.CharField(
        max_length=40,
        choices=NotificationTypes.choices,
        verbose_name="Turi"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Sarlavha"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="O'qildi"
    )

    class Meta:
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
        ordering = ['-id']

    def __str__(self):
        return f"{self.receiver} - {self.title}"
