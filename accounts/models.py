from django.db import models
from django.contrib.auth.models import AbstractUser, User

# class User(AbstractUser):
#     # AbstractUser modeli inherit qilinib, yana qo'shimcha fieldlar qo'shyapmiz
#     photo = models.ImageField()
#     date_of_birth = models.DateTimeField()
#     address = models.TextField()

# Yuqoridagi usulda migration bilan bog'liq muammolar bo'ladi. Shu sabab 1-usuldan foydalanamiz.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/",)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profili"