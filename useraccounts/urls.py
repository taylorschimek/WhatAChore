from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views
from .forms import EmailLoginForm

urlpatterns = [
    # Registration and Login URLs
    url(r'^login/$',
        views.EmailLoginView.as_view(),
        # views.ajax_login,
        name='login',
        kwargs={"form": EmailLoginForm}),

    url(r'^login-page/$',
        views.login_page,
        name='login-page'),

    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),

    url(r'^password_change/$',
        views.ChangePasswordView.as_view(),
        name='password_change'),

    url(r'^password_change/done/$',
        views.change_password_done,
        name='password_change_done'),

    url(r'^password_reset$',
        views.my_password_reset,
        # auth_views.PasswordResetView.as_view(),
        # auth_views.password_reset,
        name='password_reset'),

    url(r'^password_reset/done/$',
        # auth_views.PasswordResetDoneView.as_view(),
        # views.reset_password_redirect,
        auth_views.password_reset_done,
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(post_reset_login=True, success_url='/useraccounts/home'),
        name='password_reset_confirm'),

    url(r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    url(r'^register/', views.register, name='register-user'),

    url(r'^welcome/', views.ProfileCreateFormView.as_view(), name='welcome-new'),

    url(r'^welcome2/', views.PostProfileCreateView.as_view(), name='welcome-new2'),

    url(r'^home/$', views.HomeView.as_view(), name='home-view'),

    url(r'week/(?P<pk>\d+)$', views.OldWeekView.as_view(), name='passed-week'),

    url(r'^email/', views.email_to_worker, name='email-to-worker'),

    url(r'home/account/(?P<pk>\d+)$', views.AccountSettings.as_view(), name='account-settings'),
]
