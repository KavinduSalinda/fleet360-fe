from django.db import models
from users.models import CustomUser


class Customer(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blacklisted', 'Blacklisted'),
    ]
    
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    nic = models.CharField(max_length=20, unique=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    driving_licence_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'customers'


class CustomerDocument(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=200)
    document_hash = models.CharField(max_length=500)
    document_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.first_name} - {self.document_name}"
    
    class Meta:
        db_table = 'customer_documents'
