from django.db import models


class Post(models.Model):
	post = models.CharField(max_length=1000)