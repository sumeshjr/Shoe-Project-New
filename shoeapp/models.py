from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('supplier', 'Supplier'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='shoeapp_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='shoeapp_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image_url = models.ImageField(upload_to='product_images/', blank=True, null=True)  # For uploading images

    def __str__(self):
        return self.name
    


# Supplier Model
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supplier")
    company_name = models.CharField(max_length=200)
    contact_info = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
    
    
class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField('Product', related_name="orders")  # Many-to-Many relation with Product
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, blank=True, null=True, related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - User: {self.user.username}"

# Wishlist Model
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    products = models.ManyToManyField(Product, related_name="wishlisted_by")

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(Product, through='CartItem', related_name="in_carts")

    def __str__(self):
        return f"{self.user.username}'s Cart"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField()
    size = models.IntegerField(choices=[(i, str(i)) for i in range(5, 13)]) 

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

# Invoice Model
class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_file = models.FileField(upload_to="invoices/")
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for Order {self.order.id}"

class ProductUpdateRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="update_requests")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="product_update_requests")

    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Update Request for {self.product.name} by {self.supplier.company_name}"
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
#ChatBot_Model
class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username}: {self.user_message[:30]}"
    

