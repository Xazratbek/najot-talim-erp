from django.db import models
from django.contrib.auth.models import AbstractUser
from branches.models import Branch

class Roles(models.TextChoices):
    ADMIN = "admin", "Admin"
    STUDENT = "student", "O'quvchi"
    TEACHER = "teacher", "O'qituvchi"
    SUPPORT_TEACHER = "support_teacher", "Yordamchi o'qituvchi"

class GenderChoices(models.TextChoices):
    MALE = "male", "Erkak"
    FEMALE = "female","Ayol"

class User(AbstractUser):
    username = models.CharField(
        max_length=5,
        unique=True,
        verbose_name="Login"
    )
    phone = models.CharField(
        max_length=20,
        unique=True
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=30,
        choices=Roles.choices
    )
    balance = models.PositiveIntegerField(default=0)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    gender = models.CharField(max_length=15,null=True,blank=True,choices=GenderChoices.choices)
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-id']

    def __str__(self):
        return self.username