from django.db import models

from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product

NULLABLE = {'null': True, 'blank': True}


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, **NULLABLE)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        _items = self.get_items_cached  # Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = self.get_items_cached  # Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.product_cost, _items)))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
