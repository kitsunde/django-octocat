import json
import urllib
from django.core.urlresolvers import reverse
from django.test import TestCase
from httmock import HTTMock
from mock import patch
from github.exceptions import BadVerificationCode
from github.factories import ApplicationFactory, AuthenticationFactory, UserFactory
from github.models import Authentication, Application, User as GithubUser
from github.utils import get_user_model

User = get_user_model()


class TestAuthorize(TestCase):
    def setUp(self):
        self.app = ApplicationFactory()
        self.url = reverse('github:authorize', kwargs={'pk': self.app.pk})

    def test_redirects_to_github(self):
        response = self.client.get(self.url)
        params = urllib.urlencode({
            'state': '1',
            'redirect_uri': 'http://testserver',
            'client_id': '2134'
        })
        target_url = 'https://github.com/login/oauth/authorize?%s' % params
        # We can replace this in Django 1.7 with
        # self.assertRedirects(.., fetch_redirect_response=False)
        self.assertEqual(response['Location'], target_url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_next(self):
        response = self.client.get(self.url, {'next': '/test-url'})
        params = urllib.urlencode({
            'state': '1',
            'redirect_uri': 'http://testserver/test-url',
            'client_id': '2134'
        })
        target_url = 'https://github.com/login/oauth/authorize?%s' % params
        # We can replace this in Django 1.7 with
        # self.assertRedirects(.., fetch_redirect_response=False)
        self.assertEqual(response['Location'], target_url)
        self.assertEqual(response.status_code, 302)


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
        user_count = User.objects.count()
        self.client.get(self.url)
        self.assertEqual(user_count + 1, User.objects.count())

    @patch.object(Authentication, 'get_access_token', lambda s, a: 'foo')
    @patch.object(Application, 'request', lambda s, m, headers: {
        'id': '1',
        'login': 'testuser',
        'url': 'http://example.org/foo',
        'email': 'test@example.org'
    })
    def test_authorize_updates_access_token(self):
        user = UserFactory(application=self.authorization.application)
        self.assertNotEqual(user.access_token, 'foo')
        self.client.get(self.url)
        self.assertEqual(GithubUser.objects.get(pk=user.pk).access_token, 'foo')


class TestAuthorizeModel(TestCase):
    def setUp(self):
        self.authentication = AuthenticationFactory()

    def test_raise_exception_on_invalid_access_token(self):
        response = json.dumps({'error': 'bad_verification_code'})
        with self.assertRaises(BadVerificationCode):
            with HTTMock(lambda url, request: response):
                self.authentication.get_access_token('derp')
