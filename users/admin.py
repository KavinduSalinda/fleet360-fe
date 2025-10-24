from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()
from .models import Document


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']
    ordering = ['username']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number',)}),
    )

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['file_name', 'uploaded_by__username']
