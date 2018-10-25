# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from authentication.models import Merchant, UserProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Merchant)