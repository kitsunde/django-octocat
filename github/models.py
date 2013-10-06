import json
import urllib
from django.conf import settings
from django.db import models
import operator
import requests

# 1.4 Compatibility
from github.exceptions import BadVerificationCode

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Application(models.Model):
    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=20)
    client_secret = models.CharField(max_length=40)
    callback_url = models.URLField(help_text='Needed for auth.')
    default_scope = models.CharField(max_length=100, null=True, blank=True)

    def request(self, path, data=None, params=None, headers=None):
        base_url = 'https://api.github.com/'
        method = "get" if not data else "post"
        headers = dict(headers or {}, Accept='application/json')
        return requests.request(url="%s%s" % (base_url, path),
                                method=method,
                                data=json.dumps(data) if data else None,
                                params=params,
                                headers=headers).json()

    def __unicode__(self):
        return self.name


class Authentication(models.Model):
    application = models.ForeignKey(Application)
    redirect_uri = models.URLField(db_index=True)
    scope = models.CharField(max_length=100, null=True, blank=True)

    def get_absolute_url(self):
        base_url = 'https://github.com/login/oauth/authorize'
        auth_args = {
            'client_id': self.application.client_id,
            'redirect_uri': self.redirect_uri
        }
        if self.scope:
            auth_args['scope'] = self.scope
        elif self.application.default_scope:
            auth_args['scope'] = self.application.default_scope

        auth_args['state'] = self.pk

        return '%s?%s' % (base_url, urllib.urlencode(auth_args))

    def get_access_token(self, code):
        api = 'https://github.com/login/oauth/access_token'
        response = requests.post(api, {
            'client_id': self.application.client_id,
            'redirect_uri': self.redirect_uri,
            'client_secret': self.application.client_secret,
            'code': code
        }, headers={'Accept': 'application/json'}).json()

        if response.get('error') == 'bad_verification_code':
            raise BadVerificationCode()

        return response['access_token']


class User(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,
                             null=True,
                             blank=True,
                             related_name='github_users')
    login = models.CharField(max_length=100)
    uid = models.BigIntegerField()
    application = models.ForeignKey(Application)
    avatar_url = models.URLField()
    url = models.URLField()
    email = models.EmailField()

    access_token = models.CharField(max_length=200)

    def request(self, path, data=None, params=None, headers=None):
        params = dict(params or {}, access_token=self.access_token)
        return self.application.request(path, data, params, headers)

    def add_key(self, title, key):
        response = self.request('user/keys', {'title': title, 'key': key})
        Key(user=self).update_from_response(response)

    def update_keys(self):
        response = self.request('user/keys')
        self.keys.exclude(id__in=map(operator.itemgetter('id'),
                                     response)).delete()
        for key_data in response:
            Key(user=self).update_from_response(key_data)

    def update_user(self):
        response = self.request('user')
        self.email = response['email']
        self.url = response['url']
        self.login = response['login']
        self.save()

    def update_repositories(self):
        response = self.request('user/repos')
        self.repositories.all().delete()
        for repository in response:
            assert self.uid == repository['owner']['id']
            obj = Repository(owner=self)
            obj.update_from_response(repository)

    class Meta:
        unique_together = ('uid', 'application')

    def __unicode__(self):
        return self.login


class Key(models.Model):
    user = models.ForeignKey(User, related_name='keys')
    id = models.PositiveIntegerField(primary_key=True)
    key = models.TextField()
    url = models.URLField()
    title = models.CharField(max_length=100)

    def update_from_response(self, key_data):
        self.__dict__.update(key_data)
        self.save()

    def __unicode__(self):
        return self.title


class Repository(models.Model):
    uid = models.BigIntegerField()
    owner = models.ForeignKey(User, related_name='repositories')
    name = models.CharField(max_length=100)
    description = models.TextField()

    private = models.BooleanField()
    fork = models.BooleanField()

    url = models.URLField()
    html_url = models.URLField()
    clone_url = models.URLField()
    git_url = models.CharField(max_length=200)
    ssh_url = models.CharField(max_length=200)
    svn_url = models.URLField()
    mirror_url = models.CharField(max_length=200, null=True, blank=True)

    homepage = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)

    forks = models.PositiveSmallIntegerField(default=0)
    forks_count = models.PositiveSmallIntegerField(default=0)
    watchers = models.PositiveSmallIntegerField(default=0)
    watchers_count = models.PositiveSmallIntegerField(default=0)
    size = models.PositiveSmallIntegerField(default=0)

    master_branch = models.CharField(max_length=100, blank=True, null=True)
    open_issues = models.PositiveSmallIntegerField(default=0)

    pushed_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def refresh(self):
        """ Refresh repo details from Github """
        response = self.owner.request('repos/%s/%s' % (self.owner.login,
                                                       self.name))
        self.update_from_response(response)

    def update_from_response(self, response):
        response['uid'] = response['id']
        del response['id']
        del response['owner']
        self.__dict__.update(response)
        self.save()

    class Meta:
        unique_together = ('uid', 'owner')

    def __unicode__(self):
        return self.name