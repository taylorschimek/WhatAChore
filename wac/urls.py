from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^chores/$', views.ChoreListView.as_view(), name='chore-list'),
    url(r'^chores/create/$', views.ChoreCreateView.as_view(), name='chore-create'),
    url(r'^chores/(?P<pk>\d+)$', views.ChoreDetailView.as_view(), name='chore-detail'),
    url(r'^chores/(?P<pk>\d+)/delete$', views.ChoreDelete.as_view(), name='chore-delete'),
    url(r'^people/$', views.PeopleListView.as_view(), name='people-list'),
    url(r'^people/new/$', views.PersonCreateView.as_view(), name='person-create'),
    url(r'^people/(?P<pk>\d+)$', views.PersonDetailView.as_view(), name='person-detail'),
    url(r'^people/(?P<pk>\d+)/delete$', views.PersonDelete.as_view(), name='person-delete'),
    url(r'^lineup/$', views.lineup, name='lineup'),
]
