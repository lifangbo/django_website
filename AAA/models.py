from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

from django.utils.translation import ugettext_lazy as _


# Create your models here.
class user_ext(User):
    birthday = models.DateField(_('date bithed'), default = datetime.date.today)

    phone_number = models.CharField(_('phone number'), max_length=16, blank=True)

    is_male = models.BooleanField(_('gender'),default=False)

    province = models.CharField(_('province'), max_length=30, blank=True)

    state = models.CharField(_('state'), max_length=30, blank=True)

    street = models.CharField(_('street'), max_length=128, blank=True)


    def __str__(self):
        return self.id, self.birthday, self.phone_number, self.is_male