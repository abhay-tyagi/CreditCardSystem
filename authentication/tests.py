# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from .models import UserProfile, Merchant

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time


baseURL = 'http://127.0.0.1:8000/'

def signinHelper(selenium, arg, eml, pss):
	selenium.get('http://127.0.0.1:8000/authentication/signin/' + arg + '/')
	
	email = selenium.find_element_by_id('inputEmail')
	password = selenium.find_element_by_id('inputPassword')
	submit = selenium.find_element_by_id('loginBut')

	email.send_keys(eml)
	password.send_keys(pss)
	submit.click()


def acceptAlert(selenium):
	try:
		selenium.switch_to.alert.accept();
	except:
		pass


class AccountTestCase(LiveServerTestCase):

	def setUp(self):
		caps = DesiredCapabilities.FIREFOX.copy()
		caps["unexpectedAlertBehaviour"] = "accept"

		self.selenium = webdriver.Firefox(capabilities=caps)
		super(AccountTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(AccountTestCase, self).tearDown()


	def testB_MerchantAuth(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/authentication/signin/merchant/')
		
		selenium.find_element_by_id('signupBtn').click()

		name = selenium.find_element_by_id('name')
		email = selenium.find_element_by_id('mail')
		banklist = selenium.find_element_by_id('banklist')
		password1 = selenium.find_element_by_id('pass')
		password2 = selenium.find_element_by_id('repass')
		gstfile = selenium.find_element_by_id('gstfile')
		gstid = selenium.find_element_by_id('gstid')
		bankaccno = selenium.find_element_by_id('bankaccno')

		eml = 'abhaytyagi1998@gmail.com'
		name.send_keys('Abhay Merchant')
		email.send_keys(eml)
		banklist.send_keys('ICICI')
		password1.send_keys('qwerty')
		password2.send_keys('qwerty')
		gstfile.send_keys("/home/abhay/Downloads/IdCard.jpg")
		gstid.send_keys('123456')
		bankaccno.send_keys('123456')
		selenium.find_element_by_id('submitBtn').click()

		acceptAlert(selenium)
		self.assertTrue(selenium.current_url in ('http://127.0.0.1:8000/authentication/signin/merchant/', 'http://127.0.0.1:8000/authentication/signup/'))

		selenium.get('http://127.0.0.1:8000/authentication/activate/merchant/')		
		acceptAlert(selenium)
		self.assertTrue(selenium.current_url in ('http://127.0.0.1:8000/authentication/activate/merchant/', 'http://127.0.0.1:8000/authentication/signin/merchant/'))

		signinHelper(selenium, 'merchant', eml, 'qwerty')
		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')


	def testA_CustomerAuth(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/authentication/signin/customer/')
		
		selenium.find_element_by_id('signupBtn').click()

		name = selenium.find_element_by_id('custname')
		email = selenium.find_element_by_id('custmail')
		banklist = selenium.find_element_by_id('custbanklist')
		password1 = selenium.find_element_by_id('pass1')
		password2 = selenium.find_element_by_id('repass1')
		panno = selenium.find_element_by_id('pannum') 
		bankaccno = selenium.find_element_by_id('custaccno')
		credno = selenium.find_element_by_id('credno')

		eml = 'sabhay1@student.nitw.ac.in'
		name.send_keys('Abhay Customer')
		email.send_keys(eml)
		banklist.send_keys('HDFC')
		password1.send_keys('qwerty')
		password2.send_keys('qwerty')
		panno.send_keys('JPAN69')
		bankaccno.send_keys('234567')
		credno.send_keys('234567')
		selenium.find_element_by_id('submitBtn1').click()

		acceptAlert(selenium)
		self.assertTrue(selenium.current_url in ('http://127.0.0.1:8000/authentication/signin/customer/', 'http://127.0.0.1:8000/authentication/signup/'))

		selenium.get('http://127.0.0.1:8000/authentication/activate/customer/')		
		acceptAlert(selenium)
		self.assertTrue(selenium.current_url in ('http://127.0.0.1:8000/authentication/activate/customer/', 'http://127.0.0.1:8000/authentication/signin/customer/'))

		signinHelper(selenium, 'merchant', eml, 'qwerty')
		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')


	def testD_PasswordChange(self):
		selenium = self.selenium

		signinHelper(selenium, 'merchant', 'abhaytyagi1998@gmail.com', 'qwerty')
		selenium.get('http://127.0.0.1:8000/authentication/changePassword/')

		oldPass = selenium.find_element_by_id('opass')
		newPass1 = selenium.find_element_by_id('npass')
		newPass2 = selenium.find_element_by_id('renpass')

		oldPass.send_keys('qwerty')
		newPass1.send_keys('qwerty')
		newPass2.send_keys('qwerty')

		selenium.find_element_by_id('submitBtn').click()

		acceptAlert(selenium)
		self.assertTrue(selenium.current_url in ('http://127.0.0.1:8000/', 'http://127.0.0.1:8000/authentication/changePassword/'))
