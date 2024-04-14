from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=32)

    def __str__(self):
        return  self.name


class Material(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return  self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)


class PartialWarehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)


