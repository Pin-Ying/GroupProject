from django.db import models

# Create your models here.

class movies(models.Model):
    id=models.CharField(max_length=20,primary_key=True,null=False,unique=True)
    title=models.CharField(max_length=100)
    screen=models.CharField(max_length=20)
    area=models.CharField(max_length=100)
    theater=models.CharField(max_length=100)

    def __str__(self):
        return self.title