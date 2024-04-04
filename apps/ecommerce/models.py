from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.get_full_name()
    
    def get_full_name(self):
        return self.user.get_full_name()

class Employee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.get_full_name()
    
    def get_full_name(self):
        return self.user.get_full_name()

class ProductCategory(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to="product-categories", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM da CATEGORIA:", self.name)
            url=''
        return url

class Gender(models.Model):
    name = models.CharField(max_length=30,  null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

class Size(models.Model):
    name = models.CharField(max_length=5, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20, null=False)
    description = models.TextField()
    value_hexadecimal = models.CharField(max_length=7, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.value_hexadecimal}"


    
class Sale(models.Model):
    title = models.CharField(max_length=100)
    percentage_value = models.FloatField()
    expiration_date = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.percentage_value}"
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to="products", null=True, blank=True)

    category = models.ManyToManyField(to=ProductCategory)
    gender = models.ManyToManyField(to=Gender)
    color = models.ManyToManyField(to=Color)
    size = models.ManyToManyField(to=Size)
    sale = models.ForeignKey(to=Sale, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM do PRODUCTO:", self.name)
            url=''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.customer}"


    
class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.order}"

class Review(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
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