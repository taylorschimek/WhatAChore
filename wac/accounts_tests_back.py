from datetime import date
from django_webtest import WebTest
from time import sleep
import webtest

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase
from django.test.client import Client

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .forms import *
from .models import *
from useraccounts.models import User


class UseraccountsTests(StaticLiveServerTestCase):

    fixtures = ['wac/fixtures/wac.json', 'useraccounts/fixtures/useraccounts.json']

    @classmethod
    def setUpClass(cls):
        super(UseraccountsTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UseraccountsTests, cls).tearDownClass()

    def test_registeration(self):
        driver = self.selenium

        driver.get('{}{}'.format(self.live_server_url, reverse('landing')))
        driver.find_element_by_xpath("//a[text()='Register']").click()
        reg_email = driver.find_element_by_id('reg_email')
        reg_email.send_keys('sample@email.com')
        reg_pass = driver.find_element_by_id('reg_password')
        reg_pass.send_keys('samplepass')

        driver.find_element_by_xpath("//button[text()='SIGN UP FOR FREE']").click()
        self.assertIn('useraccounts/welcome/', driver.current_url)

        # On welcome/create first worker page
        driver.find_element_by_id('id_name').send_keys('John')
        birthday = driver.find_element_by_id('id_birthday')
        birthday.clear()
        birthday.send_keys('1990-01-01')
        driver.find_element_by_xpath("//select[@id='id_day_off']/option[text()='Friday']").click()
        driver.find_element_by_xpath("//input[@value='Save']").click()

        self.assertIn('wac/people/', driver.current_url)
        try:
            myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-title')))
            actual = myElem.text
        except TimeoutException:
            print('loading card-title took too long')

        self.assertEqual(actual, 'John')

        driver.find_element_by_xpath("//a[text()='Logout - sample@email.com']").click()

        # Try to register, but try to register email already in use.
        try:
            reg_email = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'reg_email')))
        except TimeoutException:
            print('loading reg_email took too long')
        reg_email.send_keys('sample@email.com')
        reg_pass = driver.find_element_by_id('reg_password')
        reg_pass.send_keys('bingbong')

        driver.find_element_by_xpath("//button[text()='SIGN UP FOR FREE']").click()
        self.assertIn('useraccounts/register/#registration', driver.current_url)

        driver.get('{}{}'.format(self.live_server_url, '/useraccounts/register'))
        test = driver.find_element_by_xpath("//h1[@class='display-3']").text
        self.assertEqual(test, 'Blame It On Us')

    def test_home_view_and_change_password(self):
        """ Test home view and change password flow """
        driver = self.selenium

        driver.get('{}{}'.format(self.live_server_url, reverse('landing')))
        driver.find_element_by_xpath("//a[text()='Login']").click()
        try:
            reg_email = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'id_username')))
        except TimeoutException:
            print('reg_email took too long to load')
        reg_email.send_keys('test1@example.com')
        reg_pass = driver.find_element_by_id('id_password')
        reg_pass.send_keys('password1')
        driver.find_element_by_xpath("//input[@value='Login']").click()
        try:
            profiled = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'profiled')))
            profiled_text = profiled.text
        except TimeoutException:
            print('profiled took too long to load')
        self.assertEqual(profiled_text, 'Bob')

        # Password Change Flow
        try:
            AS_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'acctSettings')))
        except TimeoutException:
            print('account settings took too long')
        AS_button.click()
        try:
            button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Change Password']")))
            button.click()
        except TimeoutException:
            print('change password took too long to load')

        try:
            old_pass = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'id_old_password')))
            old_pass.send_keys('password1')
        except TimeoutException:
            print('old_password took too long')
        driver.find_element_by_id('id_new_password1').send_keys('changed1')
        driver.find_element_by_id('id_new_password2').send_keys('changed1')
        driver.find_element_by_id('myFormSubmitButton').click()
        self.assertIn('useraccounts/home/', driver.current_url)
        sleep(5)
        # log out
        try:
            logout_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Logout - test1@example.com']")))
            logout_button.click()
        except TimeoutException:
            print("logout button took too long")


        # log back in
        driver.find_element_by_xpath("//a[text()='Login']").click()
        try:
            reg_email = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'id_username')))
        except TimeoutException:
            print('reg_email took too long to load')
        reg_email.send_keys('test1@example.com')
        reg_pass = driver.find_element_by_id('id_password')
        reg_pass.send_keys('changed1')
        driver.find_element_by_xpath("//input[@value='Login']").click()
        try:
            profiled = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'profiled')))
            profiled_text = profiled.text
        except TimeoutException:
            print('profiled took too long to load')
        self.assertEqual(profiled_text, 'Bob')




    def test_login_page(self):
        """ Test login-page """
        driver = self.selenium
        driver.get('{}{}'.format(self.live_server_url, reverse('login-page')))

        # login from login_page
        try:
            reg_email = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'id_username')))
        except TimeoutException:
            print('reg_email took too long to load')
        reg_email.send_keys('test1@example.com')
        reg_pass = driver.find_element_by_id('id_password')
        reg_pass.send_keys('password1')
        driver.find_element_by_xpath("//input[@value='Login']").click()
        try:
            profiled = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'profiled')))
            profiled_text = profiled.text
        except TimeoutException:
            print('profiled took too long to load')
        self.assertEqual(profiled_text, 'Bob')
