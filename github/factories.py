import factory

from .models import Application, Authentication, User


class ApplicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Application

    name = 'test'
    client_id = '2134'
    client_secret = 'safsdfdsf'
    callback_url = 'http://testserver'


class AuthenticationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Authentication

    application = factory.SubFactory(ApplicationFactory)
    redirect_uri = 'http://testserver'
    scope = ''


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    login = 'test'
    uid = 1
    application = factory.SubFactory(ApplicationFactory)
    avatar_url = 'http://example.org/foo.png'
    url = 'http://example.org/foo'
    email = 'foo@example.org'
