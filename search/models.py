from django.db import models

# Create your models here.
### 演員、劇院資料


class movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    img_src = models.CharField(max_length=100, null=True)
    trailer_link=models.CharField(max_length=100, null=True)
    main_actor=models.CharField(max_length=100, null=True)
    info = models.CharField(max_length=100, null=True)
    release_date = models.DateField(max_length=100, null=True)
    running_time = models.CharField(max_length=100, null=True)
    screen_type = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title
    
class theater(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address=models.CharField(max_length=100, null=True)
    phone=models.IntegerField(null=True)
    

    def __str__(self):
        return self.name

class user(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.EmailField()
    

    def __str__(self):
        return self.account
