from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
