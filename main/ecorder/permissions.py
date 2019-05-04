from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Order

"""
Permission for Order, it is different from Product, only orderer can see own' order.
"""


class OrderCompositionPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'POST':
            if 'ecorder.add_order' in request.user.get_group_permissions():
                return True

        if request.method in ['GET', 'DELETE', 'PUT']:
            obj = get_object_or_404(
                Order.objects.filter(id=view.kwargs['pk']))
            return obj.customer == request.user

        return False
