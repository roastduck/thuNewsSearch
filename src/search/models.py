from django.db import models

class Pages(models.Model):
    htmlurl = models.CharField(max_length = 300)
    date = models.CharField(max_length = 20)
    title = models.CharField(max_length = 50)
    columnName = models.CharField(max_length = 20)
    content = models.TextField()

class Inverted(models.Model):
    page = models.ForeignKey(Pages)
    key = models.CharField(max_length = 10)

