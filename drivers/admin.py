from django.contrib import admin
from .models import Driver, DriverDocument


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver_id', 'first_name', 'last_name', 'email', 'is_available']
    list_filter = ['is_available', 'country']
    search_fields = ['first_name', 'last_name', 'email', 'nic']
    readonly_fields = ['driver_id', 'created_at', 'updated_at']


@admin.register(DriverDocument)
class DriverDocumentAdmin(admin.ModelAdmin):
    list_display = ['driver', 'document_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['driver__first_name', 'driver__last_name', 'document_name']
