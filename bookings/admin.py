from django.contrib import admin
from .models import Booking, BookingAddOn, BookingReturn, BookingExtension, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['location_id', 'name', 'address']
    search_fields = ['name', 'address']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'customer', 'vehicle', 'status', 'booking_date', 'return_date']
    list_filter = ['status', 'driving_type', 'fuel_responsibility', 'insurance_type', 'booking_date']
    search_fields = ['booking_id', 'customer__first_name', 'customer__last_name', 'vehicle__registration_no']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']


@admin.register(BookingAddOn)
class BookingAddOnAdmin(admin.ModelAdmin):
    list_display = ['booking', 'add_on_name', 'add_on_price']
    list_filter = ['add_on_name']


@admin.register(BookingReturn)
class BookingReturnAdmin(admin.ModelAdmin):
    list_display = ['booking', 'return_date', 'is_damage', 'refunded_deposit_amount']
    list_filter = ['is_damage', 'return_date']


@admin.register(BookingExtension)
class BookingExtensionAdmin(admin.ModelAdmin):
    list_display = ['booking', 'original_return_date', 'extend_return_date', 'no_of_extend_days', 'price']
    list_filter = ['original_return_date', 'extend_return_date']
