from django.urls import reverse
from django.test import TestCase
from .models import User

class InvalidUserInfoTest(TestCase):

    def invalid_email(self):
        u = User(username='buddy1', password='password', email='buddyatgmail.com')
        u.save()
        if(teams.filter(username='buddy1')):
            self.assertTrue('@' not in u.email)

    def invalid_first_name(self):
        u = User(username='buddy2', password='password', first_name='123', email='buddy@gmail.com')
        u.save()
        if(teams.filter(username='buddy2')):
            self.assertFalse(any(c.isalpha() for c in u.first_name))

    def invalid_last_name(self):
        u = User(username='buddy3', password='password', last_name='123', email='buddy@gmail.com')
        u.save()
        if(teams.filter(username='buddy3')):
            self.assertFalse(any(c.isalpha() for c in u.last_name))

class ValidUserInfoTest(TestCase):
    def valid_email(self):
        u = User(username='buddy4', password='password', email='buddy@gmail.com')
        u.save()
        if(teams.filter(username='buddy4')):
            self.assertTrue('@' in u.email)
            self.assertTrue('.' in u.email)
            self.assertTrue(any(c.isalpha() for c in u.email))

    def valid_first_name(self):
        u = User(username='buddy5', password='password', first_name='buddy', email='buddy@gmail.com')
        u.save()
        if(teams.filter(username='buddy5')):
            self.assertTrue(c in 'abcdefghijklmnopqrstuvwxyz' for c in u.first_name)

    def valid_last_name(self):
        u = User(username='buddy6', password='password', last_name='friend', email='buddy@gmail.com')
        u.save()
        if(teams.filter(username='buddy6')):
            self.assertTrue(c in 'abcdefghijklmnopqrstuvwxyz' for c in u.last_name)