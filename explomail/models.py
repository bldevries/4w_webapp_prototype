from django.db import models

import datetime


class Client(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100, unique=True)


# Create your models here.
class Mail(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    sender = models.CharField(max_length=200, blank=True)
    receiver = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField('date send', blank=True, null=True)
    chronological_order = models.IntegerField()
    subject = models.CharField(max_length=1000, blank=True)
    text = models.CharField(max_length=50000)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    client_code = models.CharField(max_length=200, blank=True)
    study = models.CharField(max_length=200, blank=True)
    data_set = models.CharField(max_length=200, blank=True)
