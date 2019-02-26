from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


class SystemUser(AbstractUser):
    email = models.EmailField(unique=True)
    birthday = models.DateField(verbose_name="Birthday date", blank=True)
    avatar = models.ImageField(verbose_name="Avatar", upload_to='Avatars', blank=True)

    is_ceo = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)

    activation_key = models.CharField(max_length=128, blank=True, editable=False)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)), editable=False)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
