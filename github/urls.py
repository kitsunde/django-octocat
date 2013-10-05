# flake8:noqa
from django.conf.urls import *
from github.views import AuthorizeView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/authorize$', AuthorizeView.as_view(), name='authorize'),
)
