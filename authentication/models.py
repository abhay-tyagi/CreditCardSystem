# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from Website.models import * 
 
# Create your models here.

private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	credit_card_number = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
	credit_score = models.DecimalField(decimal_places=2, max_digits=10, default=0)
	pan_number = models.CharField(max_length=10)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
	account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
	activation_code = models.CharField(max_length=50, default='user')	

	def __str__(self):
		return str(self.user.get_full_name())


class Merchant(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
	govt_id = models.FileField(storage=private_storage, null=True)
	gst_id = models.CharField(max_length=50)
	account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
	activation_code = models.CharField(max_length=50, default='merchant') 

	def __str__(self):
		return str(self.user.get_full_name())