from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from users.user_manager import CustomUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUser(AbstractBaseUser):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    email = models.EmailField(unique=True)
    web = models.URLField(null=True)
    password = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects=CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'auth_user'
