import marshmallow

from django.db import models

# Create your models here.

class Deal(models.Model):
    customer = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()

class Client(marshmallow.Schema):
    username = marshmallow.fields.Str()
    spent_money = marshmallow.fields.Int()
    gems = marshmallow.fields.List(cls_or_instance=marshmallow.fields.Dict())



