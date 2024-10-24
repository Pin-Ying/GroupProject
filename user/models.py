from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class CustomUser(models.Model):
    name = models.CharField(max_length=255)
    account = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    preferences = models.TextField()  # 儲存使用者的電影偏好（可以是JSON格式）
    verification_code = models.CharField(max_length=6)  # 用於驗證
    verificationok = models.BooleanField(default=False)
