import factory

from .models import Application, Authentication


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
