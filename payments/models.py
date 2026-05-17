from django.db import models
from users.models import User
from common.models import TimeStampedModel

class PaymentTypeChoices(models.TextChoices):
    NAQD = "naqd", "Naqd"
    CLICK = "click", "Click"
    PAYME = "payme", "Payme"
    CARD = "card", "Karta"
    OTHER = "other", "Boshqa"

class Payment(TimeStampedModel):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    payment_type = models.CharField(max_length=25,choices=PaymentTypeChoices.choices)
    paid_at = models.DateTimeField()

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-id']

    def __str__(self):
        return str(self.amount)