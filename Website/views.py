# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *
from authentication.models import *
from .utilities import Read_qr
import decimal
import datetime

# Create your views here.

def index(request):
	if request.user.is_authenticated:
		return render(request, 'Website/index.html', {})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})

def pendingFunds(request):
	if request.user.is_authenticated:
		trans = Transaction.objects.filter(merchant__user=request.user, status=False)

		pends = {}
		todays = []

		for tran in trans:
			if tran.date == datetime.date.today():
				todays.append(tran)
			else:
				if tran.date in pends:
					pends[str(tran.date)] += float(tran.amount)
				else:
					pends[str(tran.date)] = float(tran.amount)

		return render(request, 'Website/pendingFunds.html', {'pends': pends, 'todays': todays[::-1]})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})


def payPending(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			dt = request.POST['date']
			amt = request.POST['amt']
 
			ft = FundTransfer()
			ft.merchant = Merchant.objects.get(user=request.user)
			ft.bank = ft.merchant.bank
			ft.amount = amt
			ft.save()

			merc = ft.merchant.account
			merc.usage += decimal.Decimal(amt)
			merc.save()

			trans = Transaction.objects.filter(date=dt)
			for tran in trans:
				tran.status = True
				tran.save()

			msg = "Hello " + request.user.get_full_name() + "\nYou have paid the Transfer Fee of Rs. " + str(amt) + " for " + str(dt) + ".\nYou will receive the funds for the transactions within 3 hours. "

			try:
				send_mail('Funds Transferred', msg, 'abyswp@gmail.com', [ft.merchant.user.email], fail_silently=False,)
			except:
				pass


		trans = Transaction.objects.filter(merchant__user=request.user, status=False)

		pends = {}
		todays = []

		for tran in trans:
			if tran.date == datetime.date.today():
				todays.append(tran)
			else:
				if tran.date in pends:
					pends[str(tran.date)] += float(tran.amount)
				else:
					pends[str(tran.date)] = float(tran.amount)

		return render(request, 'Website/pendingFunds.html', {'pends': pends, 'todays': todays[::-1]})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})



def scanCard(request):
	if request.user.is_authenticated:
		try:
			cardNumber = Read_qr.funct()
		except:
			return redirect('/')

		try:
			card = CreditCard.objects.get(card_number=cardNumber)
			return render(request, 'Website/intermediary.html', {'card': card, 'flag': 0})
		except CreditCard.DoesNotExist:
			return render(request, 'Website/index.html', {})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})


def transactionFinal(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			amt = request.POST['amount']
			pin = request.POST['pin']
			cardno = request.POST['cardno']
			cust = request.POST['cardown']

			card = CreditCard.objects.get(card_number=cardno)
			account = UserProfile.objects.get(credit_card_number__card_number=cardno)
			account = account.account

			if str(card.pin) != str(pin):
				return render(request, 'Website/intermediary.html', {'card': card, 'flag': amt})
			elif card.blocked == True or card.expiry_date < datetime.date.today():
				return render(request, 'Website/intermediary.html', {'card': card, 'flag': 'failed'}) 
			elif account.usage + decimal.Decimal(float(amt)) > account.max_limit:
				return render(request, 'Website/intermediary.html', {'card': card, 'flag': 'overflow'})
 
			trans = Transaction()
			trans.amount = amt
			trans.credit_card = card
			trans.merchant = Merchant.objects.get(user=request.user)
			trans.customer = UserProfile.objects.get(user__username=cust)

			acc = trans.customer.account
			acc.usage += decimal.Decimal(float(trans.amount))

			trans.save()
			acc.save() 

			msg = "Amount debited for a purchase of " + str(amt) + " from " + trans.merchant.user.get_full_name()

			try:
				send_mail('Purchase made', msg, 'abyswp@gmail.com', [trans.customer.user.email], fail_silently=False,)
			except:
				pass

			return render(request, 'Website/transactionFinal.html', {'trans': trans})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})