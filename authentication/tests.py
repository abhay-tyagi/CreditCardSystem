# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from .models import UserProfile, Merchant
import time


class AccountTestCase(LiveServerTestCase):

	def setUp(self):
		self.selenium = webdriver.Firefox()
		super(AccountTestCase, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(AccountTestCase, self).tearDown()


	def testMerchantAuth(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/authentication/signin/merchant/')
		
		signupButton = selenium.find_element_by_id('signupBtn')
		signupButton.click()

		name = selenium.find_element_by_id('name')
		email = selenium.find_element_by_id('mail')
		banklist = selenium.find_element_by_id('banklist')
		password1 = selenium.find_element_by_id('pass')
		password2 = selenium.find_element_by_id('repass')
		gstfile = selenium.find_element_by_id('gstfile')
		gstid = selenium.find_element_by_id('gstid')
		bankaccno = selenium.find_element_by_id('bankaccno')
		submit = selenium.find_element_by_id('submitBtn')

		name.send_keys('Abhay Merchant')
		email.send_keys('abhaytyagi1998@gmail.com')
		banklist.send_keys('ICICI')
		password1.send_keys('qwerty')
		password2.send_keys('qwerty')
		gstfile.send_keys("/home/abhay/Downloads/IdCard.jpg")
		gstid.send_keys('123456')
		bankaccno.send_keys('123456')
		submit.click()

		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/authentication/signin/merchant/')

		selenium.get('http://127.0.0.1:8000/authentication/activate/merchant/')		
		selenium.switch_to_alert().accept();

		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/authentication/signin/merchant/')

		selenium.get('http://127.0.0.1:8000/authentication/signin/merchant/')
		
		email = selenium.find_element_by_id('inputEmail')
		password = selenium.find_element_by_id('inputPassword')
		submit = selenium.find_element_by_id('loginBut')

		email.send_keys('abhaytyagi1998@gmail.com')
		password.send_keys('qwerty')
		submit.click()

		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')


	def testCustomerAuth(self):
		selenium = self.selenium
		selenium.get('http://127.0.0.1:8000/authentication/signin/customer/')
		
		signupButton = selenium.find_element_by_id('signupBtn')
		signupButton.click()

		name = selenium.find_element_by_id('custname')
		email = selenium.find_element_by_id('custmail')
		banklist = selenium.find_element_by_id('custbanklist')
		password1 = selenium.find_element_by_id('pass1')
		password2 = selenium.find_element_by_id('repass1')
		panno = selenium.find_element_by_id('pannum') 
		bankaccno = selenium.find_element_by_id('custaccno')
		credno = selenium.find_element_by_id('credno')
		submit = selenium.find_element_by_id('submitBtn1')

		name.send_keys('Abhay Customer')
		email.send_keys('sabhay1@student.nitw.ac.in')
		banklist.send_keys('HDFC')
		password1.send_keys('qwerty')
		password2.send_keys('qwerty')
		panno.send_keys('JPAN69')
		bankaccno.send_keys('234567')
		credno.send_keys('234567')
		submit.click()

		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/authentication/signin/customer/')

		selenium.get('http://127.0.0.1:8000/authentication/activate/customer')		
		selenium.switch_to_alert().accept();

		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/authentication/signin/customer/')

		selenium.get('http://127.0.0.1:8000/authentication/signin/customer/')
		
		email = selenium.find_element_by_id('inputEmail')
		password = selenium.find_element_by_id('inputPassword')
		submit = selenium.find_element_by_id('loginBut')

		email.send_keys('sabhay1@student.nitw.ac.in')
		password.send_keys('qwerty')
		submit.click()

		self.assertEqual(selenium.current_url, 'http://127.0.0.1:8000/')