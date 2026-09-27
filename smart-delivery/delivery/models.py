import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# 1. جدول المستخدمين والأدوار
class User(AbstractUser):
  ROLE_CHOICES = (
      ('admin', 'Admin'),
      ('dispatcher', 'Dispatcher'),
      ('driver', 'Driver'),
      ('customer', 'Customer'),
  )
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

  def __str__(self):
      return f'{self.username} ({self.get_role_display()})'


# 2. جدول العملاء
class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=50)
  address = models.TextField()

  def __str__(self):
      return self.name


# 3. جدول السائقين
class Driver(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=50)
  vehicle_type = models.CharField(max_length=100)
  is_available = models.BooleanField(default=True)

  def __str__(self):
      return f'{self.name} - {self.vehicle_type}'


# 4. جدول الشحنات
class Delivery(models.Model):
  STATUS_CHOICES = (
      ('PENDING', 'Pending'),
      ('ASSIGNED', 'Assigned'),
      ('IN_TRANSIT', 'In Transit'),
      ('DELIVERED', 'Delivered'),
      ('DELAYED', 'Delayed'),
      ('CANCELLED', 'Cancelled'),
  )

  tracking_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='deliveries')
  pickup_address = models.TextField()
  dropoff_address = models.TextField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
  driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  scheduled_date = models.DateTimeField()
  VEHICLE_CHOICES = [
    ('big_van', 'مركلة (كبيرة)'),
    ('van', 'مركبة'),
    ('moto', 'موتوسيكل (خفيف)'),
    ]

  vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, null=True, blank=True)
  notes = models.TextField(null=True, blank=True)

  def __str__(self):
      return f'{self.tracking_number} - {self.customer}'



# 5. جدول سجل الحالات (بيتسجل تلقائيًا من delivery/signals.py)
class StatusHistory(models.Model):
  delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='history')
  old_status = models.CharField(max_length=20, choices=Delivery.STATUS_CHOICES, null=True, blank=True)
  new_status = models.CharField(max_length=20, choices=Delivery.STATUS_CHOICES)
  changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  changed_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f'{self.delivery_id}: {self.old_status} -> {self.new_status}'


# 6. جدول الشات بوت
class ChatMessage(models.Model):
  SENDER_ROLES = (
      ('user', 'User'),
      ('assistant', 'Assistant'),
      ('tool', 'Tool'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
  role = models.CharField(max_length=20, choices=SENDER_ROLES)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f'{self.user} [{self.role}]: {self.content[:40]}'
