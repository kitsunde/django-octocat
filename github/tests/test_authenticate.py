from django.core.urlresolvers import reverse
from django.test import TestCase
from github.factories import ApplicationFactory


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
