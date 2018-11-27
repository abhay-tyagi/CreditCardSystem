# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import LiveServerTestCase

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


	def testC_Transaction(self):
		selenium = self.selenium

		signinHelper(selenium, 'merchant', 'abhaytyagi1998@gmail.com', 'qwerty')

		selenium.execute_script("document.getElementById('credcardno').value = '234567'")
		selenium.execute_script("document.getElementById('NoSubmit').click()")

		self.assertTrue(selenium.current_url == baseURL or 'scanCard' in selenium.current_url)

		element_present = EC.presence_of_element_located((By.ID, "amount"))
		WebDriverWait(selenium, 10).until(element_present)

		amtField = selenium.find_element_by_id('amount')
		amtField.send_keys('100')
		selenium.find_element_by_id('restBtn').click()

		pinField = selenium.find_element_by_id('pin')
		pinField.send_keys('1111')
		selenium.find_element_by_id('pinBtn').click()

		self.assertTrue('transactionFinal' in selenium.current_url or selenium.current_url == baseURL)
