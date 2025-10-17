from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['file_name', 'uploaded_by__username']
