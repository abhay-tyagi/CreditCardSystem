# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Bank(models.Model):
	name = models.CharField(max_length=50)
	location = models.CharField(max_length=50)
	ifsc = models.CharField(max_length=12)
	branch_name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class CreditCard(models.Model):
	card_number = models.IntegerField()
	cvv = models.IntegerField()
	expiry_date = models.DateField()
	blocked = models.BooleanField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

	def __str__(self):
		return self.card_number


class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	credit_card_number = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    pin = forms.IntegerField()
    credit_score = models.DecimalField()
    pan_number = models.CharField(max_length=10)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.first_name



class Merchant(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
	




