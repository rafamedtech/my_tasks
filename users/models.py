from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Create your models here.
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, _perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='profile-images', null=True, blank=True)
    fb_profile = models.CharField(max_length=100, null=True, blank=True)
    twitter_profile = models.CharField(max_length=100, null=True, blank=True)
    linkedin_profile = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'