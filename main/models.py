from django.contrib.auth.models import AbstractUser
from django.db import models


class PermaLinkModel(models.Model):
    url = models.CharField(max_length=120, blank=True, null=True)


class CustomUserModel(AbstractUser):
    permalink = models.ForeignKey(PermaLinkModel, on_delete=models.CASCADE, null=True, blank=True)
