from django.db import models
from common.models import TimeStampedModel
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Lesson(TimeStampedModel):
    title = models.CharField(max_length=255,db_index=True)
    lesson_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def get_average_rating(self):
        result = self.ratings.aggregate(Avg('star'))
        return result['star__avg'] or 0.0

class LessonRating(TimeStampedModel):
    lesson =  models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='ratings',db_index=True)
    rated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews',db_index=True)
    star = models.IntegerField(validators=[MinValueValidator(1,message="Eng kam baxo 1 bo'lishi kerak"),MaxValueValidator(5,message="Eng ko'pi bilan naxo 5 bo'lishi mumkin")],db_index=True)
    description = models.TextField()

    def __str__(self):
        return f"Dars: {self.lesson.title}-baxosi: {self.star} | Rated by: {self.rated_by.get_full_name()}"
