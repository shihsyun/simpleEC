from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .permissions import OrderCompositionPermission


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (OrderCompositionPermission,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
