import uuid
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from apps.vendor.models import Vendor
from django.db.models.signals import post_save
from apps.userauths.models import User, Profile


PRODUCT_STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

PAYMENT_STATUS = (
    ("paid", "Paid"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("cancelled", "Cancelled"),
    ("initiated", 'Initiated'),
    ("failed", 'failed'),
    ("refunding", 'refunding'),
    ("refunded", 'refunded'),
    ("unpaid", 'unpaid'),
    ("expired", 'expired'),
)

ORDER_STATUS = (
    ("Pending", "Pending"),
    ("Fulfilled", "Fulfilled"),
    ("Partially Fulfilled", "Partially Fulfilled"),
    ("Cancelled", "Cancelled"),
)

PRODUCT_REVIEW_RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)

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
    

class Product(models.Model):
    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products",default='defaults/product.png', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    stock_quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    status = models.CharField(max_length=30,choices=PRODUCT_STATUS, default="published")
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
    
    def update_rating(self) -> None:
        self.rating = self.product_rating()

    def __str__(self) -> str:
        return self.title 
    

    @property
    def get_imageURL(self) -> str:
        try:
            url = self.image.url
        except:
            print("## ERRO CARREGANDO A IMAGEM:", self.__str__())
            url = ''
        return url
    
    def product_rating(self):
        product_rating = Review.objects.filter(product=self).aggregate(avg_rating=models.Avg("rating"))
        return product_rating['avg_rating']
    
    def rating_count(self):
        return Review.objects.filter(product=self).count()

    def gallery(self):
        return Gallery.objects.filter(product=self)
    
    def specification(self):
        return Specification.objects.filter(product=self)
    
    def size(self):
        return Size.objects.filter(product=self)
    
    def color(self):
        return Color.objects.filter(product=self)


def product_image_directory(instance, filename):
    return f'products/{instance.product.title}/{filename}'

class Gallery(models.Model):
    gid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_directory, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Imagens de Produto"
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


class Specification(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Especificações de Produto"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Espec. de {self.product} - {self.title}"

class Size(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tamanhos de Produto"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Tam. de {self.product} - {self.name}"

class Color(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cores de Produto"
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Tam. de {self.product} - {self.name}"

class Coupon(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=255, null=False, blank=False)
    discount = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cupons e Promoções"
        ordering = ['-created_at', 'vendor']
    
    def __str__(self) -> str:
        return f"{self.code}"  

class Cart(models.Model):
    cid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    country = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    cart_id = models.CharField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Carrinhos"
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.cart_id} - {self.product} - {self.user}"
    
class CartOrder(models.Model):
    oid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vendor = models.ManyToManyField(Vendor)
    buyer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default="initiated")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")

    #Stripe
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Coupons
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Bio Data
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)

    # Shipping Address
    country = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    municipe = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Ordens de Produtos"
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.oid}"
    
    def order_items(self):
        return CartOrderItem.objects.filter(order=self)

class CartOrderItem(models.Model):
    oiid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey(to=CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(to=Vendor, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    country = models.CharField(max_length=100, null=True, blank=True) # remove

    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)

    # Coupons
    coupon = models.ManyToManyField(Coupon, blank=True)
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Itens de Ordens"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.id}"
    
class ProductFaq(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Perguntas Frequentes de Productos"
        ordering = ['-created_at']
    def __str__(self) -> str:
        return f"FAQ de:{self.user}, Produto:{self.product}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    review = models.TextField()
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=None, choices=PRODUCT_REVIEW_RATING)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Classificações de Produtos"
        ordering = ['-created_at', 'user']
    
    def __str__(self) -> str:
        return f"Classif.:{self.product}"

    def profile(self):
        return Profile.objects.get(user=self.user)
    

@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    if instance.product:
        instance.product.update_rating()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Listas de Desejos"
        ordering = ['-created_at', 'user']
    
    def __str__(self) -> str:
        return f"{self.user} - {self.product}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(to=CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(to=CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    seen = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Notificações"
        ordering = ['-created_at', 'user']
    
    def __str__(self) -> str:
        if self.order:
            return f"Notif. {self.order}"
        return f"Notificação {self.id}"
    
class Tax(models.Model):
    country = models.CharField(max_length=100, null=True, blank=True)
    rate = models.IntegerField(default=5, help_text="Estes numeros estão em percentagens. Ex: 5%")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Taxs"
        ordering = ['country','-created_at',]
    
    def __str__(self) -> str:
        return f"{self.country} - {self.rate}"