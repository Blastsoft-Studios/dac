from django.test import TestCase
from django.conf import settings
from importlib import import_module
from django.core.urlresolvers import reverse
from htmlvalidator.client import ValidatingClient


TEST_DATA = {
    'inputName': 'DAC - 6646',
    'inputToken': 'MjYyMzM1MjgwMTAxNTg4OTkz.C0B-Tw.0J159xIK9y8C1udbCmJl99aIpRU',
    'inputAvatarFile': open('/websites/dac/static/images/test.png', 'rb'),
}

class TestGets(TestCase):
    def setUp(self):
        self.vclient = ValidatingClient()

    def test_get_views(self):
        response = self.vclient.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class SessionTestCase(TestCase):
    def setUp(self):
        # http://code.djangoproject.com/ticket/10899
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key


class TestPosts(SessionTestCase):
    def test_avatar_post(self):
        session = self.session
        session['recaptchaverified'] = True
        session.save()
        response = self.client.post('/avatar/', TEST_DATA)
        print(response.content)
        self.assertEqual(response.status_code, 200)
