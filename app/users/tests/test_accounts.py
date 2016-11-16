from django.urls import reverse
from django.test import TestCase
from .models import User

class InvalidUserInfoTest(TestCase):

    def invalid_email(self):
        u = User(username='buddy1', password='password', email='buddyatgmail.com')
        u.save()
        if(teams.filter(username='buddy1')):

#could be fixtures
class InvalidUserInfoTest(TestCase):
    def invalid_email(self):
        u = User(username='buddy1', password='password', email='buddyatgmail.com')
        u.save()
        if(users.filter(username='buddy1')):
            self.assertTrue('@' not in u.email)

    def invalid_first_name(self):
        u = User(username='buddy2', password='password', first_name='123', email='buddy@gmail.com')
        u.save()
        if(users.filter(username='buddy2')):
            self.assertFalse(any(c.isalpha() for c in u.first_name))

    def invalid_last_name(self):
        u = User(username='buddy3', password='password', last_name='123', email='buddy@gmail.com')
        u.save()
        if(users.filter(username='buddy3')):
            self.assertFalse(any(c.isalpha() for c in u.last_name))

class ValidUserInfoTest(TestCase):
    def valid_email(self):
        u = User(username='buddy4', password='password', email='buddy@gmail.com')
        u.save()
        if(users.filter(username='buddy4')):
            self.assertTrue('@' in u.email)
            self.assertTrue('.' in u.email)
            self.assertTrue(any(c.isalpha() for c in u.email))

    def valid_first_name(self):
        u = User(username='buddy5', password='password', first_name='buddy', email='buddy@gmail.com')
        u.save()

        if(users.filter(username='buddy5')):
            self.assertTrue(all(c.isalpha() for c in u.first_name))

    def valid_last_name(self):
        u = User(username='buddy6', password='password', last_name='friend', email='buddy@gmail.com')
        u.save()
        if(users.filter(username='buddy6')):
            self.assertTrue(all(c.isalpha() for c in u.last_name))

class UniqueUsersTest(TestCase):
    def unique_user(self):
        u1 = User(username='same', password='password')
        u2 = User(username='same', password='password')
        u1.save()
        u2.save()
        user_count = User.objects.all().count()
        if(users.filter(username='same')):
            self.assertEqual(user_count, 1)

#THIS MEANS WE NEED FORM VALIDATION FOR UNIQUE EMAILS
class UniqueEmailTest(TestCase):
    def unique_email(self):
        u1 = User(username='buddy1', password='password', email='same@same.com')
        u2 = User(username='buddy2', password='password', email='same@same.com')
        u1.save()
        u2.save()
        user_count = User.objects.all().count()
        if(users.filter(username='same')):
            self.assertEqual(user_count, 2)

class NoInjectionsPleaseTest(TestCase):
    def sanitization(self):
        u = User(username='()buddy()', password='?!password?!')
        u.username.translate(None, '()?!')
        u.password.translate(None, '()?!')
        u.save()
        if(users.filter(username='buddy')):
            self.assertEqual(u.username, 'buddy')
