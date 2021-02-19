from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from decimal import Decimal
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(_('name'), max_length=512)
    description = models.CharField(_('description'), max_length=1000)
    email = models.EmailField(_('email'), max_length=1000, unique=True)
    btc_wallet_address = models.CharField(_('btc wallet address'), max_length=35)
    btc_wallet_balance = models.DecimalField(_('btc wallet balance'),
                                            default = Decimal('0.0000000000'),
                                            max_digits=18, 
                                            decimal_places=10,
                                            
                                            )
    eth_wallet_address = models.CharField(_('eth wallet address'), max_length=42)
    eth_wallet_balance = models.DecimalField(_('eth wallet balance'), 
                                            default = Decimal('0.0000000000'),
                                            max_digits=18, 
                                            decimal_places=10,
                                            )
    max_amount_per_transaction = models.DecimalField(_('max amount per transaction'), 
                                            default = Decimal('10000'), 
                                            max_digits=10, 
                                            decimal_places=2)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')







