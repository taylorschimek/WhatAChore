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


class AssignmentsTests(WebTest):

    fixtures = ['wac/fixtures/wac.json', 'useraccounts/fixtures/useraccounts.json']

    @classmethod
    def setUp(cls):
        cls.client = Client()

    # @classmethod
    # def tearDown(cls):

    def test_assignment_make(self):
        """ Testing creation of assignments.
            All intervals represented.
            User = test1@example.com
        """
        self.client.login(email='test1@example.com', password='password1')
        resp = self.client.get(reverse('lineup-make'))
        assignments = Assignment.objects.all()
        print(len(assignments))
        self.assertGreater(len(assignments), 0)

    def test_assignment_make2(self):
        """ Testing creation of assignments.
            All subintervals represented.
            User = test2@example.com; Password = password2
        """
        self.client.login(email='test2@example.com', password='password2')
        resp = self.client.get(reverse('lineup-make'))
        assignments = Assignment.objects.all()
        chores = Chore.objects.filter(
            user = 16
        )
        print('Chores = {}'.format(len(chores)))
        print('Asses = {}'.format(len(assignments)))
        self.assertEqual(len(chores), 12)
        self.assertTrue(10 <= len(assignments) <= 12)

    def test_no_workers(self):
        """
            Testing trying to get assignments without having any workers.
            User = test3@example.com; password = password2
            No Workers.
        """
        self.client.login(email='test3@example.com', password='password2')
        resp = self.client.get(reverse('lineup-make'), user='test3@example.com')
        # resp = self.app.get(reverse('lineup-make'), user='test3@example.com')
        assignments = Assignment.objects.all()
        chores = Chore.objects.filter(
            user = 17
        )
        print("resp.content = {}".format(str(resp.context)))
        self.assertEqual(len(chores), 2)
        self.assertEqual(len(assignments), 0)
        self.assertEqual(resp.status_code, 302)
