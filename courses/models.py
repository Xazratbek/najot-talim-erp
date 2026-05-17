from django.db import models
from common.models import TimeStampedModel

class CourseCategory(TimeStampedModel):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Course(TimeStampedModel):
    category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE,related_name='courses')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12,decimal_places=2)

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"
        ordering = ['-id']

    def __str__(self):
        return self.title