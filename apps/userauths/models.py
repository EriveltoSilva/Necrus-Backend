import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    # reset_token  = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs) -> None:
        email_username, _ = self.email.split('@')
        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        return super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="profile", default="default/default-user.png", null=True, blank=True)
    full_name = models.CharField(max_length=255, null=False, blank=False)
    birthday = models.DateField(null=True, blank=True)
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
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.full_name
        return super(Profile, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.full_name if self.full_name else self.user.full_name)
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)