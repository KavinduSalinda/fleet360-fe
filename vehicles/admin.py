from django.contrib import admin
from .models import Vehicle, VehicleCategory, VehicleSubCategory, VehicleDocument, VehicleImage


@admin.register(VehicleCategory)
class VehicleCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name']


@admin.register(VehicleSubCategory)
class VehicleSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['sub_category_id', 'category', 'sub_category_name']
    list_filter = ['category']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_id', 'vehicle_name', 'make', 'model', 'registration_no', 'status', 'is_undermaintanace']
    list_filter = ['status', 'is_undermaintanace', 'fuel_type', 'transmission', 'category']
    search_fields = ['vehicle_name', 'make', 'model', 'registration_no', 'vin']
    readonly_fields = ['vehicle_id', 'created_at', 'updated_at']


@admin.register(VehicleDocument)
class VehicleDocumentAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'document_type', 'created_at']
    list_filter = ['document_type', 'created_at']
    search_fields = ['vehicle__vehicle_name', 'vehicle__registration_no']


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['vehicle__vehicle_name', 'vehicle__registration_no']
