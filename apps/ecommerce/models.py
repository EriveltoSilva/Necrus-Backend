from typing import Iterable
import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

ORDER_STATUS = (
    ("PROCESSANDO", "PROCESSANDO"),
    ("ENVIADO", "ENVIADO"),
    ("ENTREGUE", "ENTREGUE"),
)

PRODUCT_REVIEW_RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
    )


# class Customer(models.Model):
#     user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
#     image = models.ImageField(upload_to="clientes", null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['user']

#     def __str__(self) -> str:
#         return self.get_full_name()
    

#     def get_full_name(self):
#         return self.user.get_full_name()
    
#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except ValueError as e:
#             print(f'## ERRO CARREGANDO A IMAGEM DA CLASS "{self.__class__.__name__}":', self.get_full_name())
#             url = '/static/assets/img/user.png'
#         return url



# class Employee(models.Model):
#     user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True)
#     image = models.ImageField(upload_to="employees", null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['user']

#     def __str__(self) -> str:
#         return self.get_full_name()
    
#     def get_full_name(self):
#         return self.user.get_full_name()


######################################################## Size, Color, Gender ##################################################################################### 
# class Size(models.Model):
#     name = models.CharField(max_length=5, null=False, unique=True)
#     description = models.TextField()
#     is_published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name_plural="Tamanhos"
    #     ordering = ['name']

#     def __str__(self) -> str:
#         return self.name

# class Color(models.Model):
#     name = models.CharField(max_length=20, null=False, unique=True)
#     value_hexadecimal = models.CharField(max_length=7, null=False, unique=True)
#     is_published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name_plural="Cores"
    #     ordering = ['name']
    
#     def __str__(self) -> str:
#         return f"{self.name} - {self.value_hexadecimal}"

# class Gender(models.Model):
#     name = models.CharField(max_length=30,  null=False, unique=True)
#     description = models.TextField()
#     is_published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name_plural="Gêneros"
    #     ordering = ['name']

#     def __str__(self) -> str:
#         return self.name
    
    
# class Sale(models.Model):
#     name = models.CharField(max_length=100)
#     percentage_value = models.FloatField()
#     expiration_date = models.DateTimeField(null=False)
#     is_published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     verbose_name_plural="Promoções"
    #     ordering = ['-created_at']

#     def __str__(self) -> str:
#         return f"{self.percentage_value}"

######################################################## ProductCategory, Product, ProductImage ##################################################################################### 
class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=100, null=False)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="category", null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="Categorias de Produto"
        ordering = ['-created_at', 'title','description']
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("ecommerce:product-category",args=(self.slug,))

    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM da CATEGORIA:", self.__str__())
            url = ''
        return url
    

#Nota, fazer signal para old_price antes de salvar o novo preço
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    categories = models.ManyToManyField(to=ProductCategory)
    
    price = models.DecimalField(max_digits=15, decimal_places=2)
    old_price = models.DecimalField(max_digits=15, decimal_places=2, default="10000")
    

    in_stock = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # verbose_name="Produto"
        verbose_name_plural="Produtos"
        ordering = ['-created_at', 'title','description']

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title 
    
    def get_absolute_url(self):
        return reverse("ecommerce:detail",args=(self.slug,))
    
    def get_percentage(self):
        return (self.price/self.old_price)*100

    
    @property
    def get_imageURL(self):
        try:
            # images = self.productimage_set.all()
            # url = images[0].image.url
            url = self.image.url
        except:
            print("## ERRO CARREGANDO A IMAGEM:", self.__str__())
            url = ''
        return url

def product_image_directory(instance, filename):
    return f'products/{instance.title}/{filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_directory, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # verbose_name = "Imagens de Produto"
        verbose_name_plural = "Imagens de Produtos"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Imagem de {self.product}"
    
    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM do PRODUCTO:", self.product)
            url=''
        return url




######################################################## Order, OrderItem ##################################################################################### 
class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PROCESSANDO")
    paid_status = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Ordem de Produtos"
    
    def save(self, *args, **kwargs) -> None:
        ## logica para setar o "price", o "transaction_id", o "complete"
        return super().save(*args, **kwargs)

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
    
    @property
    def get_cart_items(self):
        return self.orderitem_set.all()
            

    
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Items das Ordens"

    def __str__(self) -> str:
        return f"{self.id} - {self.order}"
    
    @property
    def get_total(self) -> float:
        return self.product.price * self.quantity
    
    @property
    def get_imageURL(self):
        return self.product.get_imageURL
    




######################################################## ProductReview, Wishlist, Address #################################################################################### 
class ProductReview(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=PRODUCT_REVIEW_RATING, default=None)
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Avaliações de Produtos"

    def __str__(self) -> str:
        return f'{self.user}-{self.product}'
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Lista de Desejos"
    
    def __str__(self) -> str:
        return f'{self.user}-{self.product}'


class Address(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)
#     order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
#     state = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     zipcode = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Endereços"    

    def __str__(self) -> str:
        return f'{self.user},Endereco: {self.address}'



######################################################## Partner,Carousel, Address #################################################################################### 
class Partner(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to="apoiadores", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at",]
        verbose_name_plural = "Parceiros"

    def __str__(self) -> str:
        return self.name
    
    @property
    def get_imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print(f"## ERRO CARREGANDO A IMAGEM da {self.__class__.__name__}:", self.name)
            url=''
        return url
    
class Carousel(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(default="")
    image = models.ImageField(upload_to="carousel/", blank=True)
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
    def get_imageURL(self):
        try:
            url = self.image.url
        except ValueError as e:
            print("## ERRO CARREGANDO A IMAGEM DO Carousel:", self.title)
            url=''
        return url 
    