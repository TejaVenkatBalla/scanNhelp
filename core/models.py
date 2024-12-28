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

    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Product(models.Model):

    tag_id = models.IntegerField(unique=True)
    tag_type = models.IntegerField(blank=True)

    #common
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    display = models.BooleanField(default=True)  # True to show the details
    
    #contact info
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    contact_alternate_number = models.CharField(max_length=15, null=True, blank=True)
    contact_address = models.TextField(null=True, blank=True)
    
    #reward section only for tag_type=1
    note = models.TextField(null=True, blank=True)  
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    
    # Medical details only for tag_type=2
    Emergency_Contact = models.CharField(max_length=15,null=True,blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    existing_health_issues = models.TextField(null=True, blank=True)
    existing_medication = models.TextField(null=True, blank=True)
    primary_doctor = models.CharField(max_length=255, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    physically_disabled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Assign owner's details to contact info fields if they are not already set
        if not self.contact_name:
            self.contact_name = self.owner.name
        if not self.contact_phone:
            self.contact_phone = self.owner.phone
        if not self.contact_alternate_number:
            self.contact_alternate_number = self.owner.alternate_number
        if not self.contact_address:
            self.contact_address = self.owner.address
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
