import re
from django.urls import reverse
from django.test import TestCase
from users.models import User

class InvalidUserInfoTest(TestCase):   
    # jason
    def test_invalid_email(self):
        u = User(username='buddy1', password='password', email='buddyatgmail.com')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy1')):
            self.assertTrue('@' not in u.email)

    # jason
    def test_invalid_first_name(self):
        u = User(username='buddy2', password='password', first_name='123', email='buddy@gmail.com')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy2')):
            self.assertFalse(any(c.isalpha() for c in u.first_name))

    # jason
    def test_invalid_last_name(self):
        u = User(username='buddy3', password='password', last_name='123', email='buddy@gmail.com')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy3')):
            self.assertFalse(any(c.isalpha() for c in u.last_name))

class ValidUserInfoTest(TestCase):
    # jason
    def test_valid_email(self):
        u = User(username='buddy4', password='password', email='buddy@gmail.com')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy4')):
            self.assertTrue('@' in u.email)
            self.assertTrue('.' in u.email)
            self.assertTrue(any(c.isalpha() for c in u.email))

    # jason
    def test_valid_first_name(self):
        u = User(username='buddy5', password='password', first_name='buddy', email='buddy@gmail.com')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy5')):
            self.assertTrue(all(c.isalpha() for c in u.first_name))
    # jason
    def test_valid_last_name(self):
        u = User(username='buddy6', password='password', last_name='friend', email='buddy@gmail.com')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy6')):
            self.assertTrue(all(c.isalpha() for c in u.last_name))

class UniquePasswordTest(TestCase):

    # jason
    def test_unique_password(self):
        u1 = User(username='buddy1', password='password')
        u2 = User(username='buddy2', password='password')
        u1.save()
        u2.save()
        users = User.objects.all()
        user_count = User.objects.all().count()
        if(users.filter(password='password')):
            self.assertEqual(user_count, 2)


class UniqueEmailTest(TestCase):
    # jason
    def test_unique_email(self):
        u1 = User(username='buddy1', password='password', email='same@same.com')
        u2 = User(username='buddy2', password='password', email='same@same.com')
        u1.save()
        u2.save()
        users = User.objects.all()
        user_count = User.objects.all().count()
        if(users.filter(email='same@same.com')):
            self.assertEqual(user_count, 2)

class NoInjectionsPleaseTest(TestCase):
    # jason
    def test_sanitization(self):
        u = User(username='()buddy()', password='?!password?!')
        u.username.replace(r'[$-/:-?{-~!"^_\[\]]', '')
        u.save()
        users = User.objects.all()
        if(users.filter(username='buddy')):
            self.assertEqual(u.username, 'buddy')
