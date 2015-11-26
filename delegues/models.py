
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from delegues.ldap import is_authorized, get_user_info

class DegUserManager(BaseUserManager):

    def _create_user(self, username, password, is_superuser, **extra_fields):
        now = timezone.now()

        if not username:
            raise ValueError('The given username must be set')

        if not is_authorized(username):
            return None

        user = self.model(username=username, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, is_staff=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get(self, *args, **kwargs):
        user = super().get(*args, **kwargs)
        if timezone.now() - user.last_ldap_check > settings.LDAP_REFRESH:
            user.update_ldap()

        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(username, password, True, **extra_fields)

class DegUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('Sciper'), max_length=255, unique=True)
    first_name = models.CharField(_('First name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last name'), max_length=100, blank=True)
    email = models.EmailField(_('Email'), max_length=255)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    last_ldap_check = models.DateTimeField(_('last_ldap_check'))

    objects = DegUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_ldap()

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return '{} ({})'.format(self.get_full_name(), self.username)

    def get_short_name(self):
        return self.first_name

    def get_username(self):
        return self.get_full_name()

    def update_ldap(self):
        self.last_ldap_check = timezone.now()
