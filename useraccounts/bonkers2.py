# import datetime
#
# from django.contrib import auth
# from django.test import Client, TestCase
# from django.urls import reverse
#
# from .models import User
#
# # User Model Tests
# class UserModelTests(TestCase):
#     def test_user_creation(self):
#         self.test_email = 'test@example.com'
#         self.test_user = User.objects.create(
#             email=self.test_email,
#             password='password1'
#         )
#         self.assertTrue(self.test_user.pk)
#         self.assertEqual(self.test_email, self.test_user.email)
#
#
# # Registering Views Tests
# class RegisterationViewsTests(TestCase):
#     def test_registeration(self):
#         resp = self.client.post(reverse('register-user'),
#                                 {'email': 'foo@bar.com',
#                                  'password': 'password1'},
#                                  follow=True
#         )
#         user = User.objects.get(email='foo@bar.com')
#         self.assertIn('_auth_user_id', self.client.session)
#         self.assertIn(('/useraccounts/welcome/', 301), resp.redirect_chain)
#         self.assertContains(resp, 'foo@bar.com')
#
#
# class UserViewsTests(TestCase):
#     def setUp(self):
#         email = 'foo@bar.com'
#         password = 'password1'
#         self.user = User.objects.create(email=email, password=password)
#         login = self.client.login(email=email, password=password)
#         # respLogin = self.client.post(reverse('login'),
#         #                         {'email': email,
#         #                          'password': password},
#         # )
#
#     def test_home_view(self):
#         user = User.objects.get(email='foo@bar.com')
#         resp = self.client.post(reverse('home-view'))
#
#         today = datetime.date.today()
#         self.assertEqual(resp.status_code, 200)
#         self.assertContains(resp, today)
#
#
#     # def test_post_register_view(self):
#     #     self.client.login(email  c='test@example.com', password='password1')
#     #     user = User.objects.get(email='test@example.com')
#     #     resp = self.client.get(reverse('welcome-new'), user)
#     #     self.assertEqual(resp.status_code, 200)
#     #     self.assertContains(resp, 'test@example.com')
