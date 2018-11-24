# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def signin(request, arg=''):
	if request.method == 'GET':
		if arg == '':
			return render(request, 'authentication/signin.html', {'flag': 1})
		else:
			return render(request, 'authentication/signin.html', {'flag': arg, 'banks': Bank.objects.all()})
 
	elif request.method == 'POST':
		user_name = request.POST.get('username')
		password = request.POST.get('password')
		category = request.POST.get('category')

		user = authenticate(username = user_name, password = password)

		if user == None:
			return render(request, 'authentication/signin.html', {'error' : 'User-Name/Password Invalid', 'flag': category, 'banks': Bank.objects.all()})
		elif user.is_active == False:
			return render(request, 'authentication/signin.html', {'error' : 'Account not activated.', 'flag': category, 'banks': Bank.objects.all()})

		login(request, user)
		return redirect('/')

	return render(request, 'authentication/signin.html', {'flag': 1})


def signup(request):
	if request.method == 'POST':
		category = request.POST['category']

		code = category + str(random.randint(1, 99999999))
		successful = 0

		fullname = (request.POST['fullname']).split(' ')
		email = request.POST['email']
		password = request.POST['password']
		repassword = request.POST['repassword']
		bankName = request.POST['bank']
		bankaccno = request.POST['bankaccno']
		
		if User.objects.filter(username=email).exists():
			return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': 1})

		ac = Account.objects.filter(account_number=bankaccno)

		if ac.count() == 0:
			return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': 2})					
		elif Merchant.objects.filter(account=ac).exists() or UserProfile.objects.filter(account=ac).exists():
			return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': 2})					

		usr = User()
		usr.is_active = False
		usr.username = email
		usr.first_name = fullname[0]
		if len(fullname) > 1:
			usr.last_name = fullname[1]
		usr.email = email
		usr.set_password(password)
		usr.save()

		grp = Group.objects.get(name=category.capitalize()) 
		grp.user_set.add(usr)

		if category == 'merchant':
			govtID = request.FILES['govtId']
			gstID = request.POST['gstid']

			mc = Merchant()
			mc.user = usr
			mc.bank = Bank.objects.get(name=bankName)
			mc.govt_id = govtID
			mc.gst_id = gstID
			mc.account = ac[0]
			mc.activation_code = code
			mc.save() 

			successful = 1

		elif category == 'customer':
			panno = request.POST['panno']
			credno = request.POST['credno']

			print("it is")
			print(panno)

			cred = CreditCard.objects.filter(card_number=credno)

			if cred.count() == 0:
				return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': 2})

			cs = UserProfile()
			cs.user = usr
			cs.bank = Bank.objects.get(name=bankName)
			cs.account = Account.objects.get(account_number=bankaccno)
			cs.pan_number = panno
			cs.account = ac[0]
			cs.credit_card_number = cred[0]
			cs.activation_code = code
			cs.save()

			userCard = cred[0]
			userCard.owner = usr
			userCard.bank = cs.bank
			userCard.save()

			successful = 1

		if successful == 1:
			msg = "Visit\n " + str(request.META['HTTP_HOST']) + "/authentication/activate/" + code + "/ \nto activate."

			try:
				send_mail('Activate your account', msg, 'abyswp@gmail.com', [usr.email], fail_silently=False,)
			except:
				print("COULD NOT SEND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

			return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': '/signin/' + category})
		else:
			return render(request, 'Website/index.html', {})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})


def activateUser(request, arg):
	subject = None
	category  = None

	if arg[0] == 'm':
		if arg[len(arg) - 1] == 't':
			subject = Merchant.objects.all()
		else:
			subject = Merchant.objects.filter(activation_code=arg)
		category = 'merchant'
	elif arg[0] == 'c':
		if arg[len(arg) - 1] == 'r':
			subject = UserProfile.objects.all()
		else:
			subject = UserProfile.objects.filter(activation_code=arg)
		category = 'customer'

	for item in subject:
		user = User.objects.get(username=item.user.username)
		user.is_active = True
		user.save()

	return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': category})


@login_required
def changePassword(request):
	if request.method == 'GET':
		return render(request, 'authentication/changePassword.html', {})
	else:
		oldpassword = request.POST['oldpassword']
		newpassword = request.POST['newpassword']
		renewpassword = request.POST['renewpassword']

		if not check_password(oldpassword, request.user.password):
			return render(request, 'authentication/changePassword.html', {'error': 1})
		else:
			user = request.user
			user.set_password(newpassword)
			user.save()

			return render(request, 'authentication/changePassword.html', {'error': 2})


@login_required
def signout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/')
