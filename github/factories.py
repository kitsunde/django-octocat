import factory

from .models import Application


class ApplicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Application

    name = 'test'
    client_id = '2134'
    client_secret = 'safsdfdsf'
    callback_url = 'http://testserver'
