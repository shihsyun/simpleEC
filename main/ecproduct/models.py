from django.db import models
# from .managers import ProductManager
from django.conf import settings
# Create your models here.


class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        permissions = (
            ('onlyread', 'onlyread'),
            ('can_create', 'can_create'),
            ('readwrite', 'readwrite'),
        )

    def __str__(self):
        return self.title
