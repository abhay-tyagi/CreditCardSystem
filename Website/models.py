# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from authentication.models import *
import datetime

# Create your models here.

class Account(models.Model):
	account_number = models.IntegerField()
	usage = models.DecimalField(decimal_places=2, max_digits=10, default = 0)
	max_limit = models.DecimalField(decimal_places=2, max_digits=10, default=100000)

	def __str__(self):
		return str(self.id)


class Bank(models.Model):
	name = models.CharField(max_length=50)
	location = models.CharField(max_length=50)
	ifsc = models.CharField(max_length=12)
	branch_name = models.CharField(max_length=20)

	def __str__(self):
		return str(self.name)


class CreditCard(models.Model):
	card_number = models.IntegerField()
	cvv = models.IntegerField()
	expiry_date = models.DateField()
	blocked = models.BooleanField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)
	pin = models.IntegerField(null=True)

	def __str__(self):
		return str(self.card_number)


class Transaction(models.Model):
	merchant = models.ForeignKey('authentication.Merchant', on_delete=models.CASCADE)
	customer = models.ForeignKey('authentication.UserProfile', on_delete=models.CASCADE)
	time = models.TimeField(auto_now_add=True)
	date = models.DateField(default=datetime.date.today)
	amount = models.DecimalField(decimal_places=2, max_digits=10)
	credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)

	def __str__(self):
		return str(self.merchant.user.get_full_name()) + ' - ' + str(self.customer.user.get_full_name()) + ' - ' + str(self.amount)


class FundTransfer(models.Model):
	merchant = models.ForeignKey('authentication.Merchant', on_delete=models.CASCADE)
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
	date = models.DateField(default=datetime.date.today)
	time = models.TimeField(auto_now_add=True)
	amount = models.DecimalField(decimal_places=2, max_digits=10)

	def __str__(self):
		return str(self.merchant.user.get_full_name()) + ' - ' + str(self.bank.name) + ' - ' + str(self.amount)
