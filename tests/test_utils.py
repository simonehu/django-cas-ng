from __future__ import absolute_import
from django_cas_ng.utils import get_redirect_url, get_service_url
from django.test import RequestFactory

#
# get_service_url tests
#
def test_service_url_helper():
    factory = RequestFactory()
    request = factory.get('/login/')

    actual = get_service_url(request)
    expected = 'http://testserver/login/?next=/'

    assert actual == expected


def test_service_url_helper_as_https():
    factory = RequestFactory()
    kwargs = {'secure': True, 'wsgi.url_scheme': 'https', 'SERVER_PORT': '443'}
    request = factory.get('/login/', **kwargs)

    actual = get_service_url(request)
    expected = 'https://testserver/login/?next=/'

    assert actual == expected


def test_service_url_helper_with_redirect():
    factory = RequestFactory()
    request = factory.get('/login/')

    actual = get_service_url(request, redirect_to='http://testserver/landing-page/')
    expected = 'http://testserver/login/?next=http://testserver/landing-page/'

    assert actual == expected


def test_service_url_preserves_query_parameters():
    factory = RequestFactory()
    request = factory.get('/login/?foo=bar', secure=True)

    actual = get_service_url(request, redirect_to='https://testserver/landing-page/')
    assert 'next=https://testserver/landing-page/' in actual


#
# get_redirect_url tests
#
def test_redirect_url_with_url_as_get_parameter():
    factory = RequestFactory()
    request = factory.get('/login/', data={'next': '/landing-page/'})

    actual = get_redirect_url(request)
    expected = '/landing-page/'

    assert actual == expected


def test_redirect_url_falls_back_to_cas_redirect_url_setting(settings):
    settings.CAS_IGNORE_REFERER = True
    settings.CAS_REDIRECT_URL = '/landing-page/'

    factory = RequestFactory()
    request = factory.get('/login/')

    actual = get_redirect_url(request)
    expected = '/landing-page/'

    assert actual == expected


def test_params_redirect_url_preceeds_settings_redirect_url(settings):
    settings.CAS_IGNORE_REFERER = True
    settings.CAS_REDIRECT_URL = '/landing-page/'

    factory = RequestFactory()
    request = factory.get('/login/', data={'next': '/override/'})

    actual = get_redirect_url(request)
    expected = '/override/'

    assert actual == expected


def test_redirect_url_falls_back_to_http_referrer(settings):
    settings.CAS_IGNORE_REFERER = False
    settings.CAS_REDIRECT_URL = '/wrong-landing-page/'

    factory = RequestFactory()
    request = factory.get('/login/', HTTP_REFERER='/landing-page/')

    actual = get_redirect_url(request)
    expected = '/landing-page/'

    assert actual == expected


def test_redirect_url_strips_domain_prefix(settings):
    settings.CAS_IGNORE_REFERER = True
    settings.CAS_REDIRECT_URL = 'http://testserver/landing-page/'

    factory = RequestFactory()
    request = factory.get('/login/')

    actual = get_redirect_url(request)
    expected = '/landing-page/'

    assert actual == expected

