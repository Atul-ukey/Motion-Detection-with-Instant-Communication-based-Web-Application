from django.db import models

# Create your models here.
class Contact(models.Model):
    IP = models.AutoField(primary_key = True)
    whats = models.CharField(max_length = 13)