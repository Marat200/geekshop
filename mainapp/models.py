from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('-is_active',)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='Изображение', default='/products_images/default.png')
    short_desc = models.CharField(max_length=255, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Полное описание')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
