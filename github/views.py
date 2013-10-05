from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin
from models import Application, Authentication


class AuthorizeView(RedirectView, SingleObjectMixin):
    model = Application
    permanent = False
    validator = URLValidator()

    def get_redirect_url(self, **kwargs):
        application = self.get_object()

        next = self.request.REQUEST.get('next', application.callback_url)
        try:
            self.validator(next)
        except ValidationError:
            next = self.request.build_absolute_uri(next)

        authentication = Authentication.objects.create(
            application=application,
            redirect_uri=next,
        )
        return authentication.get_absolute_url()
