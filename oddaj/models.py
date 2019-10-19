from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

TYP = (
    ("fundacja", "fundacja"),
    ("organizacja pozarządowa", "organizacja pozarządowa"),
    ("zbiórka lokalna", "zbiórka lokalna"),
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return "{}" .format(self.name)

class Institution(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    typ = models.CharField(choices=TYP, default="fundacja", max_length=128)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = "Instytucja"
        verbose_name_plural = "Instytucje"

    def __str__(self):
        return "{} {};" .format(self.name, self.typ)

class Donation(models.Model):
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    adress = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=11)
    city = models.CharField(max_length=60)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = "Dar"
        verbose_name_plural = "Dary"

    def __str__(self):
        return "{} {}" .format(self.user, self.quantity)
