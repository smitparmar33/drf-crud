from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, phone,password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, phone=phone,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,email,phone, password=None,):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email,phone,password)
        user.admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True,default="")
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone']

    objects = UserManager()

    def __str__(self):
        return self.phone + self.email



    @property
    def is_admin(self):
        return self.admin

