from django.db import models
from django.conf import settings

from PIL import Image 
from .image_processing import  findDocumentContour, covert2Gray
from imutils.perspective import four_point_transform
import cv2
import numpy as np


class Shopping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    place = models.CharField(max_length=50, blank=True, null=True)
    full_price = models.DecimalField(max_digits=9, decimal_places=2)


class Item(models.Model):
    shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    item = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)


class Receipt(models.Model):
    img = models.ImageField(upload_to= "receiptImages/")

    def __str__(self):
        return "receiptPhoto"