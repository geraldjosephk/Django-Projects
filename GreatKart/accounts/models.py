from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

"""Database and migrations were erased and recreated"""


class MyAccountManager(BaseUserManager):
    """Model for creating a normal user and super user"""

    def create_user(self, first_name, last_name, username, email, password=None):
        """Normal user creation"""
        if not email:
            raise ValueError('Email required')

        if not username:
            raise ValueError('Username required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        # User permissions
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """Superuser creation"""
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        # User permissions
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """Model for user details with permissions to access custom Django admin"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13)

    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # Specifying fields on login page
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Class inheritence
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # Permissions

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
