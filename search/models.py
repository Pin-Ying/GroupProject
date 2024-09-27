from django.db import models

# Create your models here.
### 演員、劇院資料


class movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    screen = models.CharField(max_length=20, null=True)
    time = models.CharField(max_length=100, null=True)
    img_src = models.CharField(max_length=100, null=True)
    info = models.CharField(max_length=100, null=True)
    update_date = models.DateField(max_length=100, null=True)

    def __str__(self):
        return self.title
