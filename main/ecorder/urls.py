from django.urls import path
from .views import OrderViewSet


urlpatterns = [
    path('orders/', OrderViewSet.as_view(
        {'post': 'create'}), name='orders'),
    path('order/<int:pk>/', OrderViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='order'),
]
