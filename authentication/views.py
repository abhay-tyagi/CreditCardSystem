# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from .models import *

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
		elif user.is_active == False :
			return render(request, 'authentication/login.djt', {'error' : 'User is not active contact admin.', 'flag': category, 'banks': Bank.objects.all()})

		login(request, user)
		return redirect('/')

	return render(request, 'authentication/signin.html', {'flag': 1})


def signup(request):
	if request.method == 'POST':

		category = request.POST['category']

		if category == 'merchant':
			fullname = request.POST['fullname']
			email = request.POST['email']
			password = request.POST['password']
			repassword = request.POST['repassword']

			if User.objects.filter(username=email).exists():
				return render(request, 'authentication/signin.html', {'flag': category, 'banks': Bank.objects.all(), 'error': 1})


			bankName = request.POST['bank']
			govtID = request.FILES['govtId']
			gstID = request.POST['gstid']

			fullname = fullname.split(' ')

			usr = User()
			usr.username = email
			usr.first_name = fullname[0]
			if len(fullname) > 1:
				usr.last_name = fullname[1]
			usr.email = email
			usr.set_password(password)
			usr.save()

			acc = Account()
			acc.save()

			mc = Merchant()
			mc.user = usr
			mc.bank = Bank.objects.get(name=bankName)
			mc.govt_id = govtID
			mc.gst_id = gstID
			mc.account = acc
			mc.save()

			user = authenticate(username = mc.user.username, password = password)

		return render(request, 'Website/index.html', {})
	else:
		return render(request, 'authentication/signin.html', {'flag': 1})


def signout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/')
