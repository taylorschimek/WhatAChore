import datetime
from django_webtest import WebTest
from time import sleep
import webtest

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase
from django.test.client import Client

from freezegun import freeze_time

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

    def test_assignment_intervals_through_a_year(self):
        """ Testing creation of assignments starting 6-26-2017.
            All intervals represented.
            User = test1@example.com
        """
        total_assignments = 0
        monthlies_check = False
        two_monthlies_check = False
        quarterlies_check = None
        yearlies_check = False

        with freeze_time('2017-06-26'): # initial
            print('='*30)
            print('INITIAL')
            assert datetime.datetime.now() == datetime.datetime(2017, 6, 26)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('Initial test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-07-03'): # 1 wk- E2W
            print('='*30)
            print('1 week')
            assert datetime.datetime.now() == datetime.datetime(2017, 7, 3)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            print('quarterlies length = {}'.format(len(quarterlies)))

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('1 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-07-10'): # 2 wks-
            print('='*30)
            print('2 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 7, 10)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('1 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-07-17'): # 3 wks- E2W Monthly1
            print('='*30)
            print('3 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 7, 17)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if len(monthlies) == 0:
                monthlies_check = True
            else:
                self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('2 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-07-24'): # 4 wks- Monthly2
            print('='*30)
            print('4 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 7, 24)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if monthlies_check:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = False
            else:
                self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('3 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-07-31'): # 5 wks- E2W
            print('='*30)
            print('5 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 7, 31)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_months), (0,1))

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('4 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-08-07'): # 6 wks-
            print('='*30)
            print('6 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 8, 7)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('Next month/5 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-08-14'): # 7 wks- E2W 2Months1
            print('='*30)
            print('7 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 8, 14)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 0:
                two_monthlies_check = True
            else:
                self.assertEqual(len(two_months), 1)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('6 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-08-21'): # 8 wks- Monthly1 2Months2
            print('='*30)
            print('8 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 8, 21)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if len(monthlies) == 0:
                monthlies_check = True
            else:
                self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check:
                self.assertEqual(len(two_months), 1)
                two_monthlies_check = False
            else:
                self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('8 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-08-28'): # 9 wks- E2W Monthly2
            print('='*30)
            print('9 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 8, 28)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if monthlies_check:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = False
            else:
                self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_months), (0,1))

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('9 weeks out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-09-04'): # 10 wks-
            print('='*30)
            print('10 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 9, 4)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            print('quarterlies length = {}'.format(len(quarterlies)))

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('9 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-09-11'): # 11 wks- E2W Quarterly1
            print('='*30)
            print('11 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 9, 11)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            if len(quarterlies) == 0:
                quarterlies_check = 'first'
            else:
                self.assertEqual(len(quarterlies), 1)
                quarterlies_check = 'success'

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            print('quarterlies length = {}'.format(len(quarterlies)))

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('11 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-09-18'): # 12 wks- Quarterly2
            print('='*30)
            print('12 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 9, 18)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertIn(len(monthlies), (0,1))

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            if quarterlies_check == 'success':
                self.assertEqual(len(quarterlies), 0)
            else:
                if len(quarterlies) == 0:
                    quarterlies_check = 'second'
                else:
                    self.assertEqual(len(quarterlies), 1)
                    quarterlies_check = 'success'

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            print('quarterlies length = {}'.format(len(quarterlies)))

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('12 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-09-25'): # 13 wks- E2W Monthly1 Quarterly3
            print('='*30)
            print('13 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 9, 25)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if len(monthlies) == 0:
                monthlies_check = True
            else:
                self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            if quarterlies_check == 'success':
                self.assertEqual(len(quarterlies), 0)
            else:
                self.assertEqual(len(quarterlies), 1)
                quarterlies_check = None

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            print('quarterlies length = {}'.format(len(quarterlies)))

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('13 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-10-02'): # 14 wks- Monthly2
            print('='*30)
            print('14 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 2)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if monthlies_check:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = False
            else:
                self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('14 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-10-09'): # 15 wks- E2W
            print('='*30)
            print('15 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 9)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )
            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('15 week out test number of assignments = {}'.format(len(assignments)))


        with freeze_time('2017-10-16'): # 16 wks- 2Months1
            print('='*30)
            print('16 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 16)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 0:
                two_monthlies_check = True
            else:
                self.assertEqual(len(two_months), 1)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('16 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-10-23'): # 17 wks- E2W 2Months2
            print('='*30)
            print('17 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 23)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check:
                self.assertEqual(len(two_months), 1)
                two_monthlies_check = False
            else:
                self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('17 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-10-30'): # 18 wks- Monthly1
            print('='*30)
            print('18 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 10, 30)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if len(monthlies) == 0:
                monthlies_check = True
            else:
                self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('18 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-11-06'): # 19 wks- E2W Monthly2 FLAG
            print('='*30)
            print('19 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 11, 6)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if monthlies_check:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = False
            else:
                self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('19 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-11-13'): # 20 wks-
            print('='*30)
            print('20 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 11, 13)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('20 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-11-20'): # 21 wks- E2W
            print('='*30)
            print('21 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 11, 20)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('21 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-11-27'): # 22 wks-
            print('='*30)
            print('22 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 11, 27)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('22 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-12-04'): # 23 wks- E2W Monthly1 FLAG
            print('='*30)
            print('23 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 12, 4)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if len(monthlies) == 0:
                monthlies_check = True
            else:
                self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('23 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-12-11'): # 24 wks- Monthly2
            print('='*30)
            print('24 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 12, 11)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if monthlies_check:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = False
            else:
                self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('24 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-12-18'): # 25 wks- E2W 2Months1 Quarterly1
            print('='*30)
            print('25 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 12, 18)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 0:
                two_monthlies_check = True
            else:
                self.assertEqual(len(two_months), 1)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            if len(quarterlies) == 0:
                quarterlies_check = 'first'
            else:
                self.assertEqual(len(quarterlies), 1)
                quarterlies_check = 'success'

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('25 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2017-12-25'): # 26 wks- 2Months2 Quarterly2
            print('='*30)
            print('26 weeks')
            assert datetime.datetime.now() == datetime.datetime(2017, 12, 25)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check:
                self.assertEqual(len(two_months), 1)
            else:
                self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            if quarterlies_check == 'success':
                self.assertEqual(len(quarterlies), 0)
            else:
                if len(quarterlies) == 0:
                    quarterlies_check = 'second'
                else:
                    self.assertEqual(len(quarterlies), 1)
                    quarterlies_check = 'success'

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('26 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2018-01-01'): # 27 wks- E2W Quarterly3 FLAG
            print('='*30)
            print('27 weeks')
            assert datetime.datetime.now() == datetime.datetime(2018, 1, 1)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 1)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(monthlies), 0)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            if quarterlies_check == 'success':
                self.assertEqual(len(quarterlies), 0)
            else:
                self.assertEqual(len(quarterlies), 1)
                quarterlies_check = None

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('27 week out test number of assignments = {}'.format(len(assignments)))

        with freeze_time('2018-01-08'): # 28 wks- Monthly1
            print('='*30)
            print('28 weeks')
            assert datetime.datetime.now() == datetime.datetime(2018, 1, 8)
            self.client.login(email='test1@example.com', password='password1')
            resp = self.client.get(reverse('lineup-make'))
            current_week = Week.objects.get(
                is_current=True
            )
            assignments = Assignment.objects.filter(
                week=current_week
            )

            daily_asses = Assignment.objects.filter(
                what__interval='Daily'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(daily_asses), 7)

            two_days = Assignment.objects.filter(
                what__interval='Every 2 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(two_days), (3,4))

            three_days = Assignment.objects.filter(
                what__interval='Every 3 Days'
            ).filter(
                week=current_week
            )
            self.assertIn(len(three_days), (2,3))

            weeklies = Assignment.objects.filter(
                what__interval='Weekly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(weeklies), 1)

            two_weeks = Assignment.objects.filter(
                what__interval='Every 2 Weeks'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_weeks), 0)

            monthlies = Assignment.objects.filter(
                what__interval='Monthly'
            ).filter(
                week=current_week
            )
            if len(monthlies) == 0:
                monthlies_check = True
            else:
                self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 0)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 0)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))
            print('28 week out test number of assignments = {}'.format(len(assignments)))


        print("TOTAL ASSIGNMENTS FOR THE YEAR = {}".format(total_assignments))
