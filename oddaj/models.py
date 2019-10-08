from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

TYP = (
    (0, "fundacja"),
    (1, "organizacja pozarządowa"),
    (2, "zbiórka lokalna")
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return "{}" .format(self.name)

class Institution(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    typ = models.IntegerField(choices=TYP, default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return "{}" .format(self.name)

class Donation(models.Model):
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    categories = models.ManyToManyField(Category)
    institutiom = models.ForeignKey(Institution, on_delete=models.CASCADE)
    adress = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=11)
    city = models.CharField(max_length=60)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}" .format(self.user, self.quantity)
