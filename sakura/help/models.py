from django.db import models

# Create your models here.
class HelpCmd(models.Model):
    category = models.CharField(verbose_name="category", max_length=100)
    cmd = models.CharField(verbose_name="cmd", max_length=100)
    brief = models.CharField(verbose_name="brief", max_length=100)
    description = models.CharField(verbose_name="description", max_length=1000)
    usage = models.CharField(verbose_name="usage", max_length=1000)
    alias = models.CharField(verbose_name="alias", max_length=1000)
