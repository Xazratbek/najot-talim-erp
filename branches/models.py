from django.db import models
from common.models import TimeStampedModel

class Branch(TimeStampedModel):
    name = models.CharField(max_length=255,db_index=True)
    address = models.TextField()
    phone = models.CharField(
        max_length=20,
        blank=True
    )
    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"
        ordering = ['-id']

    def __str__(self):
        return self.name