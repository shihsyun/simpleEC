from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer
from .permissions import ProductCompositionPermission


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()

    permission_classes = (ProductCompositionPermission,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductListSerializer

        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    # def get_object(self):
    #     obj = get_object_or_404(Product.objects.filter(id=self.kwargs["pk"]))
    #     self.check_object_permissions(self.request, obj)
    #     return obj
