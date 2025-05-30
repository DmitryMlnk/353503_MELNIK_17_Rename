from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class Client(models.Model):
    USER_ROLES = [
        ('customer', 'Customer'),
        ('master', 'Master'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField("Client contact phone number", max_length=13, default="0")
    address = models.CharField("Client full address", max_length=200, default="")
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    age = models.PositiveIntegerField(default=18, validators=[MinValueValidator(18)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

class ServiceType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=700, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=700, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)], null=False)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='services')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey('MasterSpecialization', on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=13, default="0")
    hire_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.specialization}'

class MasterSpecialization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CarType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SparePartType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=400, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SparePart(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=700, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)], null=False)
    spare_part_type = models.ForeignKey(SparePartType, on_delete=models.CASCADE, related_name='spare_parts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL, null=True)
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    spare_part = models.ForeignKey(SparePart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        item_name = self.service.name if self.service else self.spare_part.name
        return f"{item_name} ({self.quantity})"

class Coupon(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=100, null=False)
    number = models.CharField(max_length=20, null=False)
    active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=100, null=False)
    phone_number = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    image = models.ImageField(upload_to="workers_images/", null=False, default="workers_images/default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MinValueValidator(10)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    answer_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.TextField(max_length=500, verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Полный текст')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title