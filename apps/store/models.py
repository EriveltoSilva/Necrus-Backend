import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.vendor.models import Vendor
from apps.userauths.models import User, Profile


class Category(models.Model):
    cid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100, null=False)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to="categories", default="defaults/category.png", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Categorias de Produto"
        ordering = ['-created_at','title','description']
    
    def save(self, *args, **kwargs) -> None:
        if self.slug=="" or self.slug==None:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"
    
    # def get_absolute_url(self):
    #     return reverse("ecommerce:product-category",args=(self.slug,))
#     def get_absolute_url(self):
#         return reverse("ecommerce:product-category",args=(self.slug,))

#     @property
#     def get_imageURL(self):
#         try:
#             url = self.image.url
#         except ValueError as e:
#             print("## ERRO CARREGANDO A IMAGEM da CATEGORIA:", self.__str__())
#             url = ''
#         return url

class Product(models.Model):
    STATUS = (
        ('PLANEJADO','PLANEJADO'),
        ('DESABILITADO','DESABILITADO'),
        ('EM_REVISAO','EM REVISÃO'),
        ('PUBLICADO','PUBLICADO'),
        )

    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products",default='defaults/product.png', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    categories = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    stock_quantity = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    status = models.CharField(max_length=30,choices=STATUS, default="PUBLICADO")
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural="Produtos"
        ordering = ['-created_at', 'title','description']

    def save(self, *args, **kwargs) -> None:
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        return super(Product, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title 
    
    # def get_absolute_url(self):
    #     return reverse("ecommerce:detail",args=(self.slug,))
    
    def get_percentage(self):
        return (self.price/self.old_price)*100

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except:
            print("## ERRO CARREGANDO A IMAGEM:", self.__str__())
            url = ''
        return url
