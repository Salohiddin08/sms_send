from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
    )

    def create_verify_code(self):
        code = random.randint(10000, 99999)
        UserConfirmation.objects.create(
            user=self,
            code=code
        )
        return code


class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=5)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Confirmation for {self.user.username}"