from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
