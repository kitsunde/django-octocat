from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.test import TestCase
from mock import patch
from github.factories import ApplicationFactory, AuthenticationFactory
from github.models import Authentication, Application
from django.contrib.auth import get_user_model

class TestAuthorize(TestCase):
    def setUp(self):
        self.app = ApplicationFactory()
        self.url = reverse('github:authorize', kwargs={'pk': self.app.pk})

    def test_redirects_to_github(self):
        response = self.client.get(self.url)
        self.assertRedirects(response,
                             'https://github.com/login/oauth/authorize'
                             '?state=1'
                             '&redirect_url=http%3A%2F%2Ftestserver'
                             '&client_id=2134')


class TestGithubAuthorizationMiddleware(TestCase):
    def setUp(self):
        self.authorization = AuthenticationFactory()
        self.url = "?code=foo&state=%d" % self.authorization.pk

    @patch.object(Authentication, 'get_access_token', lambda s, a: 'foo')
    @patch.object(Application, 'request', lambda s, m, headers: {
        'id': '10',
        'login': 'testuser',
        'url': 'http://example.org/foo',
        'email': 'test@example.org'
    })
    def test_authorize_created_user(self):
        User = get_user_model()
        user_count = User.objects.count()
        self.client.get(self.url)
        self.assertEqual(user_count + 1, User.objects.count())
