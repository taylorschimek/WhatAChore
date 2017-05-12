from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Registration and Login URLs
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/', views.register, name='register-user'),

]
