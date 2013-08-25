from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin
from models import Application, Authentication


class AuthorizeView(RedirectView, SingleObjectMixin):
    model = Application
    permanent = False

    def get_redirect_url(self, **kwargs):
        application = self.get_object()
        authentication = Authentication.objects.create(
            application=application,
            redirect_uri=self.request.REQUEST.get('next',
                                                  application.callback_url),
        )
        return authentication.get_absolute_url()
