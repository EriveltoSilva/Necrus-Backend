from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user']

    def __str__(self) -> str:
        return self.get_full_name()
    
    def get_full_name(self):
        return self.user.get_full_name()

class Employee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user']

    def __str__(self) -> str:
        return self.get_full_name()
    
    def get_full_name(self):
        return self.user.get_full_name()

class Supporter(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to="apoiadores", null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at",]

    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print(f"## ERRO CARREGANDO A IMAGEM da {self.__class__.__name__}:", self.name)
            url=''
        return url
    
    

class Size(models.Model):
    name = models.CharField(max_length=5, null=False, unique=True)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    value_hexadecimal = models.CharField(max_length=7, null=False, unique=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return f"{self.name} - {self.value_hexadecimal}"

class Gender(models.Model):
    name = models.CharField(max_length=30,  null=False, unique=True)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name']

    def __str__(self) -> str:
        return self.name
    
    
class Sale(models.Model):
    title = models.CharField(max_length=100)
    percentage_value = models.FloatField()
    expiration_date = models.DateTimeField(null=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.percentage_value}"
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=200, null=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="product-categories", null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'name','description']

    def __str__(self) -> str:
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("ecommerce:product-category",args=(self.slug,))
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM da CATEGORIA:", self.name)
            url=''
        return url
    
class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    price = models.FloatField()
    categories = models.ManyToManyField(to=ProductCategory)
    genders = models.ManyToManyField(to=Gender, blank=True)
    colors = models.ManyToManyField(to=Color, blank=True)
    sizes = models.ManyToManyField(to=Size, blank=True)
    sale = models.ForeignKey(to=Sale, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'name']
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        ...
    def get_absolute_url(self):
        return reverse("ecommerce:detail",args=(self.slug,))
    

class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Imagem de {self.product}"
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM do PRODUCTO:", self.name)
            url=''
        return url


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.customer}"
    
    @property
    def get_total_price(self) -> float:
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total 
    @property
    def get_total_items(self) -> int:
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total
        

    
class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.order}"
    
    @property
    def get_total(self) -> float:
        return self.product.price * self.quantity

class Review(models.Model):
    user = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    comment = models.TextField()
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}"
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.address
    

class Carrocel(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(default="")
    image = models.ImageField(upload_to="carrocel/", blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at",]

    def __str__(self) -> str:
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("ecommerce:product-category",args=(self.category.slug,))

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM DO CARROCEL:", self.title)
            url=''
        return url 