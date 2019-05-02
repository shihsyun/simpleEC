import secrets
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class ECUserManager(BaseUserManager):

    """
    User model manager where emial is the unique identifiers for authentication instead of usernames.
    """

    def create(self, email, password, **kwargs):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_('ENTER AN EMAIL BUDDY'))

        if not password:
            raise ValueError(_('ENTER A PASSWORD BUDDY'))

        email = self.normalize_email(email)
        kwargs.setdefault('is_active', False)
        user = self.model(email=email, password=password, **kwargs)
        user.set_password(password)
        user.save()

        group = Group.objects.get(name='Customer')
        user.groups.add(group)

        return user


class VerifyCodeManager(models.Manager):

    def create_verify_code(self, user):
        code = secrets.token_urlsafe(30)
        super(VerifyCodeManager, self).get_queryset().filter(
            user=user).delete()
        verifycode = self.model(user=user, code=code)
        verifycode.save()
        user.is_active = False
        user.save()
        return verifycode.code

    def verify_code(self, token):
        now = timezone.now()
        earlier = now - timedelta(days=3)
        token = token.strip('"')
        try:
            code = super(VerifyCodeManager, self).get_queryset().filter(
                created_at__range=(earlier, now)).get(code=token)
        except Exception:
            return False

        code.user.is_active = True
        code.user.save()
        code.delete()
        return True
