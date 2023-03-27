import json, os
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.password_validation import validate_password

class TryDjangoConfigTest (TestCase):
    def test_abc(self):
        try:
            secret_key = os.environ.get('DJANGO_SECTER_KEY')
            self.assertNotEqual(secret_key, 'abc_123')
        except Exception as e:
            self.fail(e)

    def test_password_strength(self):
        try:
            secret_key1 = os.environ.get('DJANGO_SECTER_KEY')
            secret_key = "abc"
            is_string = validate_password(secret_key)
        except Exception as e:
            message = f'Bad secret key {e.messages}'
            self.fail(message)
            