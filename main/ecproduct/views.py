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
