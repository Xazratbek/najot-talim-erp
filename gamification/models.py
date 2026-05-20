from django.db import models
from users.models import User

class XPReasonChoices(models.TextChoices):
    FOR_LESSON= "lesson", "Dars uchun"
    FOR_EXAM = "exam","Imtihon uchun"
    FOR_EVENT_ACTIVITY = "event", "Tadbirda qatnashgani uchun"
    FOR_HOMEWORK = "homework", "Uyga vazifa uchun"

class XP(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='xps'
    )
    amount = models.IntegerField()
    reason = models.CharField(max_length=40,choices=XPReasonChoices.choices)

    class Meta:
        db_table = 'xps'
        verbose_name = "XP"
        verbose_name_plural = "XPlar"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.amount}"

class Rating(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rating')
    level = models.IntegerField(default=1)

    class Meta:
        db_table = "student_rating"
        verbose_name = "Ko'rsatgich"
        verbose_name_plural = "Ko'rsatgichlar"

    def __str__(self):
        return f"{self.student.get_full_name()} bosqichi: {self.level}"