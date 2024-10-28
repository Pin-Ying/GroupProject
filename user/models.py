from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    img_src = models.CharField(max_length=100, blank=True, null=True)
    trailer_link = models.CharField(max_length=100, blank=True, null=True)
    movie_type = models.CharField(max_length=100, blank=True, null=True)
    main_actor = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.DateField(max_length=100, blank=True, null=True)
    running_time = models.CharField(max_length=100, blank=True, null=True)
    screen_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id}/{self.title}"

class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    account = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    preferences = models.TextField()  # 儲存使用者的電影偏好
    verification_code = models.CharField(max_length=6)  # 用於驗證
    verificationok = models.BooleanField(default=False) #是否驗證
    def __str__(self):
        return self.name

class Click(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=100)  # 儲存電影名稱
    clicked_at = models.DateTimeField(auto_now_add=True) #點選時間
    def __str__(self):
        return f"{self.user.name}/{self.movie_title}/{self.clicked_at}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.movie}/{self.content}"
