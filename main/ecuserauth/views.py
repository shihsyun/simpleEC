from .models import ECUser, VerifyCode
from .serializers import ECUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.translation import ugettext as _


@permission_classes((AllowAny,))
class CustomerRegister(CreateAPIView):
    queryset = ECUser.objects.all()
    serializer_class = ECUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['PUT'])
def SellerApply(request):

    try:
        user = ECUser.objects.get_by_natural_key(request.data.get('email'))
    except ECUser.DoesNotExist:
        raise ValueError(_('ENTER AN EMAIL BUDDY'))
    try:
        Token.objects.get(user=user)
    except Token.DoesNotExist:
        raise ValueError(_('INVALID TOKEN'))
    group = Group.objects.get(name='Seller')
    user.groups.add(group)
    user.save()
    return Response(HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((AllowAny,))
def CustomerVerifyGencode(request):
    user = ECUser.objects.get_by_natural_key(request.data.get('email'))
    return Response(VerifyCode.objects.create_verify_code(user))


@api_view(['GET'])
@permission_classes((AllowAny,))
def CustomerVerifyCode(request):
    if VerifyCode.objects.verify_code(request.GET.get('token')):
        return Response(HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((AllowAny,))
def CustomerLogin(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'please provide both username and password'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(email=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)

    user.last_login = timezone.now()
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, HTTP_200_OK)


@api_view(['POST'])
def CustomerLogout(request):

    username = request.data.get('username')

    if username is None:
        return Response({'error': 'please provide both username'}, status=HTTP_400_BAD_REQUEST)

    user = ECUser.objects.get_by_natural_key(request.data.get('username'))
    if not user:
        return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)

    if token:
        token.delete()
        return Response(HTTP_204_NO_CONTENT)

    return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def ChangePassword(request):

    username = request.data.get('username')
    oldpassword = request.data.get('oldpassword')
    newpassword = request.data.get('newpassword')

    if username is None:
        return Response({'error': 'please provide both username'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(email=username, password=oldpassword)
    if not user:
        return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)

    user.password = newpassword
    user.save()

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid Credientials'}, status=HTTP_404_NOT_FOUND)

    if token:
        token.delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, HTTP_200_OK)
