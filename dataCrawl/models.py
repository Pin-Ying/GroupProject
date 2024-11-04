from django.db import models
# Create your models here.
### 演員、劇院資料


class movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    img_src = models.CharField(max_length=500, blank=True, null=True)
    trailer_link = models.CharField(max_length=500, blank=True, null=True)
    movie_type = models.CharField(max_length=100, blank=True, null=True)
    main_actor = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.DateField(max_length=100, blank=True, null=True)
    running_time = models.CharField(max_length=100, blank=True, null=True)
    screen_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id}/{self.title}"


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
    full_title = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    site = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.movie.title}/{self.theater.name}/{self.date}"

