from django.db import models


class VehicleCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = 'vehicle_categories'


class VehicleSubCategory(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.sub_category_name
    
    class Meta:
        db_table = 'vehicle_sub_categories'


class Vehicle(models.Model):
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('auto', 'Automatic'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    vehicle_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(VehicleSubCategory, on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100)
    engine_capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    color = models.CharField(max_length=50)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_seats = models.IntegerField()
    insurance_no = models.CharField(max_length=100)
    insurance_expiry = models.DateField()
    registration_no = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    base_km_per_day = models.IntegerField()
    excess_km_charge = models.DecimalField(max_digits=10, decimal_places=2)
    registration_expiry = models.DateField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    odometer_reading = models.IntegerField(default=0)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_undermaintanace = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.make} {self.model} - {self.registration_no}"
    
    class Meta:
        db_table = 'vehicles'


class VehicleDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('registration', 'Registration'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_hash = models.CharField(max_length=500)
    document_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vehicle.vehicle_name} - {self.document_type}"
    
    class Meta:
        db_table = 'vehicle_documents'


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_imgs')
    image_hash = models.CharField(max_length=500)
    image_url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vehicle.vehicle_name} - Image"
    
    class Meta:
        db_table = 'vehicle_images'
