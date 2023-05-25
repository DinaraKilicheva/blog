from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(_("email address"), unique=True)
    age = models.PositiveIntegerField(null=True)
    image = models.ImageField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return self.get_full_name()


class SocialAccount(models.Model):
    class ProviderTypes(models.TextChoices):
        GOOGLE = "google"
        FACEBOOK = "facebook"
    
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="social_account", null=True)
    social_account = models.CharField(max_length=50, choices=ProviderTypes.choices)


class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="verification_codes", null=True, blank=True
    )
    email = models.EmailField(unique=True, null=True)
    last_sent_time = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)



class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
