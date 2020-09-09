from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')

    class Meta:
        verbose_name = 'User profile'

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.user.__str__())