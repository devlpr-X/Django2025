from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    pro_image = models.ImageField(upload_to='photos/accounts', blank=True, null=True)

    def __str__(self):
        # fall back to username if email empty
        return self.user.email if getattr(self.user, 'email', None) else self.user.username
