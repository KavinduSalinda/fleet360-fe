from rest_framework import serializers
from .models import Vehicle, VehicleDocument, VehicleImage, VehicleCategory, VehicleSubCategory


class VehicleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCategory
        fields = ['category_id', 'category_name']


class VehicleSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleSubCategory
        fields = ['sub_category_id', 'category', 'sub_category_name']


class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDocument
        fields = ['document_type', 'document_hash', 'document_url']


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['image_hash', 'image_url', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    documents = VehicleDocumentSerializer(many=True, required=False)
    vehicle_imgs = VehicleImageSerializer(many=True, required=False)
    
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_id', 'category', 'sub_category', 'vehicle_name',
            'engine_capacity', 'fuel_type', 'color', 'make', 'model',
            'transmission', 'price_per_day', 'no_of_seats', 'insurance_no',
            'insurance_expiry', 'registration_no', 'vin', 'description',
            'base_km_per_day', 'excess_km_charge', 'registration_expiry',
            'deposit_amount', 'vat_amount', 'odometer_reading', 'late_fee',
            'is_undermaintanace', 'status', 'documents', 'vehicle_imgs',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['vehicle_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        documents_data = validated_data.pop('documents', [])
        images_data = validated_data.pop('vehicle_imgs', [])
        
        vehicle = Vehicle.objects.create(**validated_data)
        
        for document_data in documents_data:
            VehicleDocument.objects.create(vehicle=vehicle, **document_data)
        
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=vehicle, **image_data)
        
        return vehicle
    
    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', [])
        images_data = validated_data.pop('vehicle_imgs', [])
        
        # Update vehicle fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update documents
        instance.documents.all().delete()
        for document_data in documents_data:
            VehicleDocument.objects.create(vehicle=instance, **document_data)
        
        # Update images
        instance.vehicle_imgs.all().delete()
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=instance, **image_data)
        
        return instance


class VehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'vehicle_name', 'make', 'is_undermaintanace']


class VehicleAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'is_available']
    
    is_available = serializers.SerializerMethodField()
    
    def get_is_available(self, obj):
        # This would need to be implemented based on booking logic
        return not obj.is_undermaintanace and obj.status == 'available'
