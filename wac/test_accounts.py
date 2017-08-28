from datetime import date
from django_webtest import WebTest
from time import sleep
import webtest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .forms import *
from .models import *
from useraccounts.models import User


def try_class_name(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None

def try_id(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None

def try_xpath(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None


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
        print("birthday = {}".format(birthday))
        # birthday.clear()
        birthday.send_keys('01011990')
        driver.find_element_by_xpath("//select[@id='id_day_off']/option[text()='Friday']").click()
        button = try_xpath(dirver, 2, "//input[@value='Save']")
        button.click()
        # driver.find_element_by_xpath("//input[@value='Save']").click()

        self.assertIn('wac/people/', driver.current_url)
        card_title = try_class_name(driver, 3, 'card-title')
        actual_card_title = card_title.text
        self.assertEqual(actual_card_title, 'John')

        driver.find_element_by_xpath("//a[text()='Logout - sample@email.com']").click()

        # Try to register, but try to register email already in use.
        reg_email = try_id(driver, 3, 'reg_email')
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
        myUsername = try_id(driver, 3, 'id_username')

        myUsername.send_keys('test1@example.com')
        myPass = driver.find_element_by_id('id_password')
        myPass.send_keys('password1')
        driver.find_element_by_xpath("//input[@value='Login']").click()
        profiled = try_id(driver, 3, 'profiled')
        profiled_text = profiled.text
        self.assertEqual(profiled_text, 'Bob')

        # Password Change Flow
        AS_button = try_id(driver, 3, 'acctSettings')
        AS_button.click()
        button = try_xpath(driver, 3, "//button[text()='Change Password']")
        button.click()

        old_pass = try_id(driver, 3, 'id_old_password')
        old_pass.send_keys('password1')
        driver.find_element_by_id('id_new_password1').send_keys('changed1')
        driver.find_element_by_id('id_new_password2').send_keys('changed1')
        driver.find_element_by_id('myFormSubmitButton').click()
        self.assertIn('useraccounts/home/', driver.current_url)
        sleep(5)
        # log out
        logout_button = try_xpath(driver, 5, "//a[text()='Logout - test1@example.com']")
        logout_button.click()

        # log back in
        driver.find_element_by_xpath("//a[text()='Login']").click()
        myUsername = try_id(driver, 3, 'id_username')
        myUsername.send_keys('test1@example.com')
        myPass = driver.find_element_by_id('id_password')
        myPass.send_keys('changed1')
        driver.find_element_by_xpath("//input[@value='Login']").click()
        profiled = try_id(driver, 3, 'profiled')
        profiled_text = profiled.text
        self.assertEqual(profiled_text, 'Bob')


    def test_login_page(self):
        """ Test login-page """
        driver = self.selenium
        driver.get('{}{}'.format(self.live_server_url, reverse('login-page')))

        # login from login_page
        myUsername = try_id(driver, 3, 'id_username')
        myUsername.send_keys('test1@example.com')
        myPass = driver.find_element_by_id('id_password')
        myPass.send_keys('password1')
        driver.find_element_by_xpath("//input[@value='Login']").click()
        profiled = try_id(driver, 3, 'profiled')
        profiled_text = profiled.text
        self.assertEqual(profiled_text, 'Bob')
