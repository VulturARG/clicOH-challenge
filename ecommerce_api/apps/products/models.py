from django.db import models


class Product(models.Model):
    """Model for Product"""

    name = models.CharField('name', max_length=255, unique=True, blank=False, null=False)
    description = models.TextField('description', max_length=1000, blank=False, null=False)
    price = models.DecimalField('price', max_digits=8, decimal_places=2)
    stock = models.IntegerField('stock')

    class Meta:
        """Meta class for Product"""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product"""

        return self.name
