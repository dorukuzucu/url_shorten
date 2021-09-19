from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, username, fullname, password=None):
        if not username:
            raise ValueError('User must have a valid username')
        if not email:
            raise ValueError('User must have a valid username')

        user = self.model(email=self.normalize_email(email),
                          username=username,
                          fullname=fullname)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fullname, password=None):
        user = self.create_user(email, username, fullname, password)
        user.is_admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=100,
        unique=True
    )
    username = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=50)
    registered_date = models.DateTimeField(auto_now_add=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"


class ShortenedUrl(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_url = models.TextField(max_length=200)
    shortened_url = models.CharField(max_length=10)

    class Meta:
        db_table = "urls"


