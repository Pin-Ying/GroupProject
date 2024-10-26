from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
### 演員、劇院資料


class movie(models.Model):
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
        return self.title


class theater(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    cinema = models.CharField(max_length=100, blank=True, null=True)
    img_src = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    transport = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class showTimeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(theater, on_delete=models.CASCADE)
    date = models.DateField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    site = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.movie.title}/{self.theater.name}/{self.date}"


class Review(models.Model):
    movie = models.ForeignKey(
        movie, on_delete=models.CASCADE, null=True
    )  # 使用 ForeignKey 关联
    content = models.TextField()

    def __str__(self):
        return f"{self.movie}/{self.content}"

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
    movie = models.ForeignKey(movie, on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True) #點選時間
    def __str__(self):
        return f"{self.user.name}/{self.movie.title}/{self.clicked_at}"
