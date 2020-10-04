from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        managed = True
