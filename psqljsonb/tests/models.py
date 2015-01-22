from ..fields import JSONBField
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=200)
    data = JSONBField()

    def __unicode__(self):
        return self.name

