from django.db import models
from django.contrib.auth.models import User


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    nic = models.CharField(max_length=20, unique=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    address = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'drivers'


class DriverDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('nic', 'NIC'),
        ('driving_license', 'Driving License'),
        ('passport', 'Passport'),
        ('other', 'Other'),
    ]
    
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=200)
    document_hash = models.CharField(max_length=500)
    document_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.driver.first_name} - {self.document_name}"
    
    class Meta:
        db_table = 'driver_documents'
