from django.db import models


class City(models.Model):
    name = models.CharField(max_length=25)
    ip_address = models.CharField(max_length=30)

    class Meta:
        unique_together = ('ip_address', 'name')

