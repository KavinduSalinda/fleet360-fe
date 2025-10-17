from django.contrib import admin
from .models import Customer, CustomerDocument


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'first_name', 'last_name', 'email', 'status', 'is_active']
    list_filter = ['status', 'is_active', 'country']
    search_fields = ['first_name', 'last_name', 'email', 'nic']
    readonly_fields = ['customer_id', 'created_at', 'updated_at']


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'document_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'document_name']
