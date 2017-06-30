import datetime
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django.test.utils import setup_test_environment

from .models import Chore, Person, User, Week
from .forms import AssignmentForm, ChoreEditForm, PersonEditForm


#### Model Tests ####

class ModelsTests(TransactionTestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('password1')
        self.user.save()
        print("User stuff = {}".format(self.user.id))
        self.client = Client()

    @classmethod
    def tearDown(self):
        User.objects.get(pk=self.user.pk).delete()
        # User.objects.all().delete()

    # Chore Create
    def test_chore_create(self):
        """test creating chore with form"""
        resp = self.client.get(reverse('chore-create'), user=self.user)
        self.assertEqual(resp.status, '200 OK')
        form = resp.forms[0]
        form['task'] = 'test chore'
        form['description'] = 'test description'
        form['duration'] = 20
        form['interval'] = 'Daily'
        form['age_restriction'] = 18
        resp = form.submit()
        chore = Chore.objects.get(description='test description')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context, None)

    # Person Create
    def test_person_create(self):
        """test creating person with form"""
        self.client.login(email='test@example.com', password='password1')
        user = User.objects.get(email='test@example.com')
        resp = self.client.get(reverse('person-create'), user=user)
        self.assertEqual(resp.status_code, 200)
        print(user)
        form = PersonEditForm(data={
            'name': 'test person',
            'birthday': '2010-03-01',
            'email': 'worker@example.com',
            'day_off': 'Wed'
        })
        self.client.post(reverse('person-create'), kwargs={'form': form}, user=user)
        self.assertTrue(form.is_valid())

        person = Person.objects.get(email='worker@example.com')
        # self.assertEqual(resp.context['people'][0].name, 'test person')

    # Week Create
    def test_week_create(self):
        """test that a week is created"""
        self.client.login(email='test@example.com', password='password1')
        user = User.objects.get(email='test@example.com')
        chore = Chore.objects.create(user=user,
                                     task='test_chore',
                                     description='test_description',
                                     duration=20,
                                     interval='Daily',
                                     age_restriction=18)
        person = Person.objects.create(user=user,
                                       name='test_person',
                                       birthday='2010-03-01',
                                       day_off='Wed')
        week = Week.create(current_user=user)
        resp = self.client.get(reverse('lineup'), follow=True, user=user)
        self.assertEqual(resp.status_code, 200)
        print("WAC = {}".format(resp))
        self.assertIn(person, resp.context['people'])
        # Assignment Create
        self.assertEqual(chore.task, resp.context['assignments'][0].what.task)


#### View/Template Tests ####
class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('password1')
        self.user.save()
        self.chore = Chore.objects.create(user=self.user,
                                     task='test_chore',
                                     description='test_description',
                                     duration=20,
                                     interval='Daily',
                                     age_restriction=18)
        self.chore2 = Chore.objects.create(user=self.user,
                                     task='test_chore2',
                                     description='test_description2',
                                     duration=10,
                                     interval='Weekly',
                                     age_restriction=10)
        self.person = Person.objects.create(user=self.user,
                                       name='test_person',
                                       birthday='2010-03-01',
                                       day_off='Wed')

    def test_redirect(self):
        """test login_required on chore views"""
        resp = self.client.get(reverse('chore-create'))
        self.assertRedirects(resp, '/useraccounts/login-page/?next=' + reverse('chore-create'))

    def test_chore_list_view(self):
        """test that chore list view can be accessed"""
        self.client.login(email='test@example.com', password='password1')
        response = self.client.get(reverse('chore-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.chore, response.context['chores'])
        self.assertIn(self.chore2, response.context['chores'])
        self.assertTemplateUsed(response, 'wac/chore_list.html')
        self.assertContains(response, self.chore.task)
        self.assertContains(response, self.chore2.task)

    def test_chore_detail_view(self):
        """test that chore detail view can be accessed"""
        self.client.login(email='test@example.com', password='password1')
        resp = self.client.get(reverse('chore-detail', kwargs={'pk': self.chore.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.chore.task)
        self.assertNotContains(resp, self.chore2.task)
        self.assertTemplateUsed(resp, 'wac/chore_detail.html')

        # test editing
        # form = self.app.get(reverse('chore-detail', kwargs={'pk': self.chore.pk})).form
        # form['task'] = 'test_chore_editted'
        # form['description'] = 'test_description_editted'
        # resp = form.submit().follow()
        # self.assertEqual(resp.request.url, 'http://localhost' + reverse('chore-list'))
        # self.assertContains(resp.context, 'test_chore_editted')
        # self.assertNotContains(resp.context, 'test_chore')

    def test_people_list_view(self):
        """test that people list view can be accessed"""
        self.client.login(email='test@example.com', password='password1')
        resp = self.client.get(reverse('people-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.person, resp.context['people'])
        self.assertTemplateUsed(resp, 'wac/people_list.html')
        self.assertContains(resp, self.person.name)

    def test_person_detail_view(self):
        """test that person detail view can be accessed"""
        self.client.login(email='test@example.com', password='password1')
        self.person2 = Person.objects.create(user=self.user,
                                       name='test_person2',
                                       birthday='2010-03-02',
                                       day_off='Fri')
        resp = self.client.get(reverse('person-detail', kwargs={'pk': self.person.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.person.name)
        self.assertTemplateUsed(resp, 'wac/person_detail.html')
        self.assertNotContains(resp, self.person2.name)
