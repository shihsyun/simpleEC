from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('title', 'sku', 'price',
                  'description', 'available', 'stock')


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('seller', 'title', 'sku', 'price',
                  'description', 'available', 'stock')
