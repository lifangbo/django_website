from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

from django.utils.translation import ugettext_lazy as _


VERIFY_TYPE = {'register', 'password'}


# Create your models here.
class user_ext(User):
    birthday = models.DateField(_('date bithed'), default = datetime.date.today)

    phone_number = models.CharField(_('phone number'), max_length=16, unique=True, blank=False)

    is_male = models.BooleanField(_('gender'),default=False)

    province = models.CharField(_('province'), max_length=30, blank=True)

    state = models.CharField(_('state'), max_length=30, blank=True)

    street = models.CharField(_('street'), max_length=128, blank=True)


    def __str__(self):
        return self.id, self.birthday, self.phone_number, self.is_male


class SmsVerify(models.Model):
    phone_number = models.CharField(max_length=40, unique=True)
    verify = models.CharField(max_length=20)
    passcode = models.CharField(max_length=10, blank=True)
    valid_expires = models.DateTimeField(null=True, blank=True)
    locked_expires = models.DateTimeField(null=True, blank=True)
