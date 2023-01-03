from django.db import models
from django.conf import settings



class Shopping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    date = models.DateField()
    place = models.CharField(max_length=50)
    full_price = models.DecimalField(max_digits=9, decimal_places=2)


class Item(models.Model):
    shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    item = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)


class Receipt(models.Model):
    #TODO
    img = models.ImageField(upload_to= "receiptImages/")

    def __str__(self):
        return "receiptPhoto"