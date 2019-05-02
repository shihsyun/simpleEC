from django.urls import path, include
from .views import ProductViewSet


urlpatterns = [
    path('products/', ProductViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='products'),
    path('product/<int:pk>/', ProductViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product'),

]
