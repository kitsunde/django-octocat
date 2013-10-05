from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^github/', include('github.urls', namespace='github')),
    url(r'^test-url$', TemplateView.as_view(template_name='index.html'), name='test'),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
)
