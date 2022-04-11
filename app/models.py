from datetime import datetime
from django.db import models


# Create your models here.
class Work(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    deadline = models.DateTimeField(null=False)
    email = models.EmailField(null=True)
    send = models.BooleanField(default=False)


class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, null=False)
    work_id = models.IntegerField(null=False)
    time = models.DateTimeField(default=datetime.now())
