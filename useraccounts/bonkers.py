from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .models import User


class useraccountsViewsTestCase(WebTest):
    def setUp(self):
        self.user = User.objects.create(email='foo@bar.com')
        self.user.set_password('password1')
        self.user.save()

    def test_login(self):
        """to test the login form"""

        user = User.objects.get(email='foo@bar.com')
        self.assertEqual(user.email, 'foo@bar.com')
        self.assertTrue(user.check_password('password1'))

        # login to the form
        form = self.app.get(reverse('login')).forms[0]
        form['username'] = user.email
        form['password'] = 'password1'
        resp = form.submit()
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.json['url'] + '/', reverse('home-view'))

    def test_bad_login(self):
        """make sure there is an error on bad login"""
        resp = self.client.post('useraccounts/login', params={'username': 'bad@username.com', 'password': 'password1'}, expect_errors=True)
        self.assertEqual(resp.status_code, 404)

    # def test_create_user(self):
    #     """test that a user can be created"""
    #     form = self.app.get(reverse('landing')).forms[1]
    #     print("this {}".format(form.fields))
    #     form['email'] = 'newUser@example.com'
    #     form['password'] = 'password1'
    #     resp = form.submit().backend='django.contrib.auth.backends.ModelBackend'
    #     print("THIS = {}".format(resp))
    #     # self.assertEqual(resp.)
