import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=13, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs) -> None:
        email_username, _ = self.email.split('@')
        if self.full_name == "" or self.first_name == None:
            self.first_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        return super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    # user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profile", default="default/default-user.png", null=True, blank=True)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    birthday = models.DateField(null=False, blank=False)
    about = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=2, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)
    city = models.CharField(max_length=2, null=True, blank=True)
    address = models.CharField(max_length=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name', '-created_at']
        verbose_name_plural = "Perfils"

    def save(self, *args, **kwargs) -> None:
        if self.full_name == "" or self.first_name == None:
            self.first_name = self.user.full_name
        return super(Profile, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.full_name if self.full_name else self.user.full_name)