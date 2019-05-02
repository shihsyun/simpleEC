from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Product


class ProductCompositionPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            return request.user.has_perm('ecproduct.onlyread')

        if request.method == 'POST':
            return request.user.has_perm('ecproduct.can_create')

        if request.method in ['DELETE', 'PUT']:
            obj = get_object_or_404(
                Product.objects.filter(id=view.kwargs['pk']))
            return obj.seller == request.user

        return False
