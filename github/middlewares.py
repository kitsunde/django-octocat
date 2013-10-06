from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from github.exceptions import BadVerificationCode
from github.models import Authentication, User


class GithubAuthorizationMiddleware(object):
    def process_request(self, request):
        if request.GET.get('code') and request.GET.get('state'):
            auth = Authentication.objects.get(pk=request.GET.get('state'))
            try:
                access_token = auth.get_access_token(request.GET['code'])
            except BadVerificationCode:
                return redirect(reverse('github:authorize', kwargs={
                    'pk': auth.application.pk
                }))

            user = auth.application.request('user', headers={
                'Authorization': 'token %s' % access_token
            })

            github_user, created = User.objects.get_or_create(
                application=auth.application,
                uid=user['id'],
                defaults={
                    'login': user['login'],
                    'url': user['url'],
                    'email': user['email'],
                    'access_token': access_token
                }
            )

            if not created:
                github_user.access_token = access_token
                github_user.save()

            authenticated_user = authenticate(github_user=github_user)
            if not authenticated_user is None:
                login(request, authenticated_user)
