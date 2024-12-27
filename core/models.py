# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    alternate_number = models.CharField(max_length=15, null=True, blank=True)  
    address = models.TextField(null=True, blank=True)

    # Medical details
    Emergency_Contact = models.CharField(max_length=15,null=True,blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    existing_health_issues = models.TextField(null=True, blank=True)
    existing_medication = models.TextField(null=True, blank=True)
    primary_doctor = models.CharField(max_length=255, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    physically_disabled = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Product(models.Model):
    tag_id = models.IntegerField(unique=True)
    tag_type = models.IntegerField(blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    display = models.BooleanField(default=True)  # True to show the details
    note = models.TextField(null=True, blank=True)  
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  

    def __str__(self):
        return self.name
