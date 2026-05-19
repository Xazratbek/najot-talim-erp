from django.db import models
from common.models import TimeStampedModel
from users.models import User
from courses.models import Course
from lessons.models import Lesson
from branches.models import Branch


class Group(TimeStampedModel):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    started_at = models.DateField()
    ended_at = models.DateField(
        blank=True,
        null=True
    )
    is_opened = models.BooleanField(default=False)
    max_students = models.PositiveIntegerField(default=28)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ['-id']

    def __str__(self):
        return self.name


class GroupTeacher(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='teachers'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_teachers'
    )
    class Meta:
        verbose_name = "Guruh o'qituvchisi"
        verbose_name_plural = "Guruh o'qituvchilari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.group} - {self.teacher}"


class GroupStudent(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_groups'
    )
    joined_at = models.DateField()

    class Meta:
        verbose_name = "Guruh o'quvchisi"
        verbose_name_plural = "Guruh o'quvchilari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.student} - {self.group}"

class GroupLesson(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='group_lessons'
    )
    lesson = models.OneToOneField(Lesson,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Guruh darsi"
        verbose_name_plural = "Guruh darslari"
        ordering = ['-id']

    def __str__(self):
        return f"{self.group}"