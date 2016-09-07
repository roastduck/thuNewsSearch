from django.db import models

class Pages(models.Model):
    id = models.IntegerField(primary_key = True)
    htmlurl = models.CharField(max_length = 300)
    date = models.CharField(max_length = 20)
    title = models.CharField(max_length = 50)
    columnName = models.CharField(max_length = 20)
    content = models.TextField()

class Inverted(models.Model):
    key = models.CharField(max_length = 10)
    pageId = models.IntegerField()

