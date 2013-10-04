from django.core.urlresolvers import reverse
from django.test import TestCase
from mock import patch
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
