from django.conf import settings
from django.db import models

from mainapp.models import Product


# class OrderQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for object in self:
#             for item in object.orderitems.select_related():
#                 item.product.quantity += item.quantity
#                 item.product.save()
#             object.is_active = False
#             object.save()
#         super().delete(*args, **kwargs)


class Order(models.Model):
    # objects = OrderQuerySet.as_manager()
    STATUS_FORMING = 'FM'
    STATUS_SEND_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'DN'
    STATUS_CANCELLED = 'CN'

    STATUSES = (
        (STATUS_FORMING, 'Формирование'),
        (STATUS_SEND_TO_PROCEED, 'Отправлен в обработку'),
        (STATUS_PROCEEDED, 'Обработан'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_DONE, 'Готов'),
        (STATUS_CANCELLED, 'Отменён'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=STATUS_FORMING, max_length=3)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product_cost, _items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_quantity': sum(list(map(lambda x: x.quantity, items))),
            'total_cost': sum(list(map(lambda x: x.product_cost, items)))
        }

    def delete(self, *args, **kwargs):
        for item in self.orderitems.all():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
