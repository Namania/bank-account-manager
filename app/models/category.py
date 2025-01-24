from django.db import models
from colorfield.fields import ColorField


class Category(models.Model):
    label = models.CharField(max_length=200)
    color = ColorField(verbose_name="Color", default="#007bff")

    def __str__(self):
        return self.label
