import datetime
from django_webtest import WebTest
from time import sleep
import webtest

from django.core.urlresolvers import reverse
from django.test.client import Client

from freezegun import freeze_time

from .forms import *
from .models import *
from useraccounts.models import User


class AssignmentsTests(WebTest):
    fixtures = ['wac/fixtures/wac.json', 'useraccounts/fixtures/useraccounts.json']

    @classmethod
    def setUp(cls):
        cls.client = Client()

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
        assignments = Assignment.objects.all()
        chores = Chore.objects.filter(
            user = 17
        )
        self.assertEqual(len(chores), 2)
        self.assertEqual(len(assignments), 0)
        self.assertEqual(resp.status_code, 302)

    def test_assignment_intervals_through_a_year(self):
        """ Testing creation of assignments starting 6-26-2017.
            All intervals represented.
            User = test1@example.com
        """
        total_assignments = 0
        monthlies_check = None
        two_monthlies_check = None
        quarterlies_check = None
        yearlies_check = False

        with freeze_time('2017-06-26'): # initial M1st
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
            self.assertEqual(len(monthlies), 1) # Monthly1st

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

        with freeze_time('2017-07-03'): # 1 wk- E2W
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

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2017-07-10'): # 2 wks- Monthly1 M15th
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
            if len(monthlies) == 1:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 2) # Monthly15th
                monthlies_check = 'success'

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

        with freeze_time('2017-07-17'): # 3 wks- E2W Monthly2
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

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

        with freeze_time('2017-07-24'): # 4 wks- Monthly3
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None

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

        with freeze_time('2017-07-31'): # 5 wks- E2W M1st 2M1st
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
            self.assertEqual(len(monthlies), 1) # Monthly1st

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
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

        with freeze_time('2017-08-07'): # 6 wks- 2Months1
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
            if len(two_months) == 0:
                two_monthlies_check = 'first'
            else:
                self.assertEqual(len(two_months), 1)
                two_monthlies_check = 'success'

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

        with freeze_time('2017-08-14'): # 7 wks- E2W Monthly1 2Months2 M15th 2M15th
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
            if len(monthlies) == 1:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 2) # Monthly15th
                monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 1)
            else:
                if len(two_months) == 1:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 2)
                    two_monthlies_check = 'success'

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

        with freeze_time('2017-08-21'): # 8 wks- Monthly2 2Months3
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
                two_monthlies_check = None
            else:
                self.assertEqual(len(two_months), 1)
                two_monthlies_check = None

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

        with freeze_time('2017-08-28'): # 9 wks- E2W Monthly3 M1st Q1st
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = None

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
            self.assertEqual(len(quarterlies), 1) # Quarterly1st

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2017-09-04'): # 10 wks-
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

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2017-09-11'): # 11 wks- E2W Quarterly1 M15th Q15th
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
            self.assertEqual(len(monthlies), 1) # Monthly15th

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
            if len(quarterlies) == 1:
                quarterlies_check = 'first'
            else:
                self.assertEqual(len(quarterlies), 2)
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

        with freeze_time('2017-09-18'): # 12 wks- Monthly1 Quarterly2
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
            if len(monthlies) == 0:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = 'success'

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

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2017-09-25'): # 13 wks- E2W Monthly2* Quarterly3 M1st 2M1st
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
            # Monthly1st
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
            else:
                if len(monthlies) == 1:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 2)
                    monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 1)

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

        with freeze_time('2017-10-02'): # 14 wks- Monthly3
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None

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

        with freeze_time('2017-10-09'): # 15 wks- E2W M15th 2M15th 2Months1
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
            self.assertEqual(len(monthlies), 1) # Monthly15th

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 1:
                two_monthlies_check = 'first'
            else:
                self.assertEqual(len(two_months), 2)
                two_monthlies_check = 'success'

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

        with freeze_time('2017-10-16'): # 16 wks- 2Months2
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
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2017-10-23'): # 17 wks- E2W Monthly1 2Months3
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
            if len(monthlies) == 0:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2017-10-30'): # 18 wks- Monthly2 M1st
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
            else:
                if len(monthlies) == 1:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 2)
                    monthlies_check = 'success'

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

        with freeze_time('2017-11-06'): # 19 wks- E2W Monthly3 FLAG
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None

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

        with freeze_time('2017-11-13'): # 20 wks- M15th
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
            self.assertEqual(len(monthlies), 1) # Monthly15th

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

        with freeze_time('2017-11-20'): # 21 wks- E2W
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

        with freeze_time('2017-11-27'): # 22 wks- Monthly1 M1st 2M1st Q1st
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
            if len(monthlies) == 1:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 1)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 1)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2017-12-04'): # 23 wks- E2W Monthly2 FLAG
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

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

        with freeze_time('2017-12-11'): # 24 wks- Monthly3 2Months1 M15th 2M15th Q15th
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = None

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 1:
                two_monthlies_check = 'first'
            else:
                self.assertEqual(len(two_months), 2)
                two_monthlies_check = 'success'

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 1)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2017-12-18'): # 25 wks- E2W 2Months2 Quarterly1
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
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2017-12-25'): # 26 wks- 2Months3 Quarterly2
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
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2018-01-01'): # 27 wks- E2W Monthly1 Quarterly3 M1st
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
            if len(monthlies) == 1:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = 'success'

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

        with freeze_time('2018-01-08'): # 28 wks- Monthly2
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

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

# --------------------------------------------------
        with freeze_time('2018-01-15'): # 29 wks- E2W Monthly3 M15th
            assert datetime.datetime.now() == datetime.datetime(2018, 1, 15)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = None

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

        with freeze_time('2018-01-22'): # 30 wks-
            assert datetime.datetime.now() == datetime.datetime(2018, 1, 22)
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

        with freeze_time('2018-01-29'): # 31 wks- E2W M1st 2M1st
            assert datetime.datetime.now() == datetime.datetime(2018, 1, 29)
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
            self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
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

        with freeze_time('2018-02-05'): # 32 wks- Monthly1
            assert datetime.datetime.now() == datetime.datetime(2018, 2, 5)
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
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = 'success'

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

        with freeze_time('2018-02-12'): # 33 wks- E2W Monthly2 2Months1 M15th 2M15th
            assert datetime.datetime.now() == datetime.datetime(2018, 2, 12)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
            else:
                if len(monthlies) == 1:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 2)
                    monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 1:
                two_monthlies_check = 'first'
            else:
                self.assertEqual(len(two_months), 2)
                two_monthlies_check = 'success'

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

        with freeze_time('2018-02-19'): # 34 wks- Monthly3 2Months2
            assert datetime.datetime.now() == datetime.datetime(2018, 2, 19)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2018-02-26'): # 35 wks- E2W 2Months3 M1st Q1st
            assert datetime.datetime.now() == datetime.datetime(2018, 2, 26)
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
            self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 1)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-03-05'): # 36 wks-
            assert datetime.datetime.now() == datetime.datetime(2018, 3, 5)
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

        with freeze_time('2018-03-12'): # 37 wks- E2W Monthly1 M15th Q15th
            assert datetime.datetime.now() == datetime.datetime(2018, 3, 12)
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
            if len(monthlies) == 1:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = 'success'

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
            self.assertEqual(len(quarterlies), 1)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-03-19'): # 38 wks- Monthly2
            assert datetime.datetime.now() == datetime.datetime(2018, 3, 19)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

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

        with freeze_time('2018-03-26'): # 39 wks- E2W Monthly3 Quarterly1 M1st 2M1st
            assert datetime.datetime.now() == datetime.datetime(2018, 3, 26)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = None

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
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

        with freeze_time('2018-04-02'): # 40 wks- Quarterly2
            assert datetime.datetime.now() == datetime.datetime(2018, 4, 2)
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

        with freeze_time('2018-04-09'): # 41 wks- E2W Quarterly3 M15th 2M15th
            assert datetime.datetime.now() == datetime.datetime(2018, 4, 9)
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
            self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 1)

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

        with freeze_time('2018-04-16'): # 42 wks- Monthly1 2Months1
            assert datetime.datetime.now() == datetime.datetime(2018, 4, 16)
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
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if len(two_months) == 0:
                two_monthlies_check = 'first'
            else:
                self.assertEqual(len(two_months), 1)
                two_monthlies_check = 'success'

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

        with freeze_time('2018-04-23'): # 43 wks- E2W Monthly2 2Months2
            assert datetime.datetime.now() == datetime.datetime(2018, 4, 23)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2018-04-30'): # 44 wks- Monthly3 2Months3 M1st
            assert datetime.datetime.now() == datetime.datetime(2018, 4, 30)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = None

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2018-05-07'): # 45 wks- E2W
            assert datetime.datetime.now() == datetime.datetime(2018, 5, 7)
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

        with freeze_time('2018-05-14'): # 46 wks- M15th
            assert datetime.datetime.now() == datetime.datetime(2018, 5, 14)
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

        with freeze_time('2018-05-21'): # 47 wks- E2W Monthly1
            assert datetime.datetime.now() == datetime.datetime(2018, 5, 21)
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
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = 'success'

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

        with freeze_time('2018-05-28'): # 48 wks- Monthly2 M1st 2M1st Q1st Y1st
            assert datetime.datetime.now() == datetime.datetime(2018, 5, 28)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
            else:
                if len(monthlies) == 1:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 2)
                    monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 1)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 1)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 1)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-06-04'): # 49 wks- E2W Monthly3
            assert datetime.datetime.now() == datetime.datetime(2018, 6, 4)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None

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

        with freeze_time('2018-06-11'): # 50 wks- M15th 2M15th Q15th Y15th
            assert datetime.datetime.now() == datetime.datetime(2018, 6, 11)
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
            self.assertEqual(len(monthlies), 1)

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(two_months), 1)

            quarterlies = Assignment.objects.filter(
                what__interval='Quarterly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(quarterlies), 1)

            yearlies = Assignment.objects.filter(
                what__interval='Yearly'
            ).filter(
                week=current_week
            )
            self.assertEqual(len(yearlies), 1)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-06-18'): # 51 wks- E2W 2Months1 ErrorYear
            assert datetime.datetime.now() == datetime.datetime(2018, 6, 18)
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
                two_monthlies_check = 'first'
            else:
                self.assertEqual(len(two_months), 1)
                two_monthlies_check = 'success'

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
            if len(yearlies) == 0:
                yearlies_check = True
            else:
                self.assertEqual(len(yearlies), 1)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-06-25'): # 52 wks- Monthly1 2Months2 Y M1st
            assert datetime.datetime.now() == datetime.datetime(2018, 6, 25)
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
            if len(monthlies) == 1:
                monthlies_check = 'first'
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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
            if yearlies_check:
                self.assertEqual(len(yearlies), 1)
                yearlies_check = False
            else:
                self.assertEqual(len(yearlies), 0)

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-07-02'): # 53 wks- E2W Monthly2 2Months3
            assert datetime.datetime.now() == datetime.datetime(2018, 7, 2)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 0)
            else:
                if len(monthlies) == 0:
                    monthlies_check = 'second'
                else:
                    self.assertEqual(len(monthlies), 1)
                    monthlies_check = 'success'

            two_months = Assignment.objects.filter(
                what__interval='Every 2 Months'
            ).filter(
                week=current_week
            )
            if two_monthlies_check == 'success':
                self.assertEqual(len(two_months), 0)
            else:
                if len(two_months) == 0:
                    two_monthlies_check = 'second'
                else:
                    self.assertEqual(len(two_months), 1)
                    two_monthlies_check = 'success'

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

        with freeze_time('2018-07-09'): # 54 wks- Monthly3 Quarterly1 M15th
            assert datetime.datetime.now() == datetime.datetime(2018, 7, 9)
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
            if monthlies_check == 'success':
                self.assertEqual(len(monthlies), 1)
                monthlies_check = None
            else:
                self.assertEqual(len(monthlies), 2)
                monthlies_check = None

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

            total_asses = len(daily_asses) + len(two_days) + len(three_days) + len(weeklies) + len(two_weeks) + len(monthlies) + len(two_months) + len(quarterlies) + len(yearlies)
            total_assignments += total_asses
            self.assertEqual(total_asses, len(assignments))

        with freeze_time('2018-07-16'): # 55 wks- E2W Quarterly2
            assert datetime.datetime.now() == datetime.datetime(2018, 7, 16)
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

        with freeze_time('2018-07-23'): # 56 wks- Quarterly3
            assert datetime.datetime.now() == datetime.datetime(2018, 7, 23)
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
