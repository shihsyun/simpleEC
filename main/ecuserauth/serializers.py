from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import ECUser
import re
from django.utils.translation import ugettext_lazy as _


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name',)


class ECUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ECUser
        fields = ('email', 'password')

    def validate_password(self, password):

        if len(password) < 5:
            raise serializers.ValidationError(_(
                'The password\'s length must more than 5.'))

        if not re.findall('\d', password):
            raise serializers.ValidationError(_(
                'The password must contain at least 1 digit.'))

        if not re.findall('[A-Z]', password):
            raise serializers.ValidationError(_(
                'The password must contain at least 1 uppercase letter.'))

        if not re.findall('[a-z]', password):
            raise serializers.ValidationError(_(
                'The password must contain at least 1 lowercase letter.'))

        return password
