from django.db import models
from product.models import Product

from .managers import KitProductManager


class Kit(models.Model):
    sku = models.CharField(max_length=50, primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'kit'
        managed = True


class KitProduct(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    discount = models.DecimalField(decimal_places=2, max_digits=10)

    objects = KitProductManager()

    class Meta:
        db_table = 'kit_products'
        managed = True
