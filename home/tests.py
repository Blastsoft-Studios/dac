from django.test import TestCase
from django.conf import settings
from importlib import import_module
from django.core.urlresolvers import reverse
from htmlvalidator.client import ValidatingClient
from io import BytesIO

bd = BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x00@\x08\x02\x00\x00\x00%\x0b\xe6\x89\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\x19tEXtSoftware\x00paint.net 4.0.134\x03[z\x00\x00\x00XIDAThC\xed\xcf\x01\r\x000\x10\x03\xa1\xf97\xdd\xc9 \x9f\x1c\x0ex;\xae\x80V@+\xa0\x15\xd0\nh\x05\xb4\x02Z\x01\xad\x80V@+\xa0\x15\xd0\nh\x05\xb4\x02Z\x01\xad\x80V@+\xa0\x15\xd0\nh\x05\xb4\x02Z\x01\xad\x80V@+\xa0\x15\xd0\nh\x05\xb4\x02\xda\xf1\xc0\xf6\x01\xcaS\xd2\xc2\xc4:\xbd\xd8\x00\x00\x00\x00IEND\xaeB`\x82')


TEST_DATA = {
    'inputName': 'DAC - 6646',
    'inputToken': 'MjYyMzM1MjgwMTAxNTg4OTkz.C0B-Tw.0J159xIK9y8C1udbCmJl99aIpRU',
    'inputAvatarFile': bd,
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
