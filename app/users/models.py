from django.db import models
from django.contrib.auth.models import User as AuthUser

class User(AuthUser):
    def get_profile(self):
        if hasattr(self, 'profile') and self.profile is not None:
            return self.profile
        profile = UserProfile()
        profile.user = self
        return profile

    class Meta:
        proxy = True
        permissions = (
            ('create_contest', 'Can create contests'),
        )

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    theme = models.URLField(null=True)
