from typing import Iterable
from django.db import models
from django.utils.text import slugify
from apps.userauths.models import User, Profile

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Nome da Loja", null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=500)
    image = models.ImageField(upload_to="vendors", default="default/default-user.png", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, help_text="Telefone da loja", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Vendedores"
        ordering = ['name', '-created_at']

    def __str__(self) -> str:
        return self.name if self.name else self.user
    
    def save(self, *args, **kwargs) -> None:
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name)
        return super(Vendor, self).save(*args, **kwargs)
