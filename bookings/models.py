from django.db import models
from customers.models import Customer
from vehicles.models import Vehicle
from drivers.models import Driver


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'locations'


class Booking(models.Model):
    DRIVING_TYPE_CHOICES = [
        ('self_drive', 'Self Drive'),
        ('need_driver', 'Need Driver'),
    ]
    
    FUEL_RESPONSIBILITY_CHOICES = [
        ('by_client', 'By Client'),
        ('by_company', 'By Company'),
    ]
    
    INSURANCE_TYPE_CHOICES = [
        ('comprehensive', 'Comprehensive'),
        ('general', 'General'),
    ]
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('flat', 'Flat'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField()
    return_date = models.DateTimeField()
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup_bookings')
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_bookings')
    starting_odometer_reading = models.IntegerField()
    is_return_to_same_location = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driving_type = models.CharField(max_length=20, choices=DRIVING_TYPE_CHOICES)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    no_of_passengers = models.IntegerField()
    fuel_responsibility = models.CharField(max_length=20, choices=FUEL_RESPONSIBILITY_CHOICES)
    deposited_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_vat_applicable = models.BooleanField(default=False)
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPE_CHOICES)
    insurance_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.customer.first_name} {self.customer.last_name}"
    
    class Meta:
        db_table = 'bookings'


class BookingAddOn(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='add_ons')
    add_on_name = models.CharField(max_length=100)
    add_on_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.booking.booking_id} - {self.add_on_name}"
    
    class Meta:
        db_table = 'booking_add_ons'


class BookingReturn(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='return_details')
    return_date = models.DateField()
    final_odometer_reading = models.IntegerField()
    is_damage = models.BooleanField(default=False)
    damage_notes = models.TextField(blank=True, null=True)
    refunded_deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Return for Booking {self.booking.booking_id}"
    
    class Meta:
        db_table = 'booking_returns'


class BookingExtension(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='extensions')
    original_return_date = models.DateField()
    extend_return_date = models.DateField()
    no_of_extend_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Extension for Booking {self.booking.booking_id}"
    
    class Meta:
        db_table = 'booking_extensions'

