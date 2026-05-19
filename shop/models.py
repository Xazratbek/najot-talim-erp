from django.db import models
from common.models import TimeStampedModel

from users.models import User

class Category(TimeStampedModel):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = "shop_categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField(db_index=True)
    image = models.ImageField(
        upload_to='products/'
    )
    stock = models.PositiveIntegerField(db_index=True)

    class Meta:
        db_table = "products"
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-id']

    def __str__(self):
        return self.title


class Order(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-id']

    def __str__(self):
        return str(self.id)