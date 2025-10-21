from rest_framework import serializers
from .models import Driver, DriverDocument


class DriverDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverDocument
        fields = ['document_name', 'document_hash', 'document_url']


class DriverSerializer(serializers.ModelSerializer):
    documents = DriverDocumentSerializer(many=True, required=False)
    
    class Meta:
        model = Driver
        fields = [
            'driver_id', 'first_name', 'last_name', 'email', 'contact_number',
            'nic', 'passport_number', 'country', 'nationality', 'address',
            'is_available', 'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['driver_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        documents_data = validated_data.pop('documents', [])
        driver = Driver.objects.create(**validated_data)
        
        for document_data in documents_data:
            DriverDocument.objects.create(driver=driver, **document_data)
        
        return driver
    
    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', [])
        
        # Update driver fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update documents
        instance.documents.all().delete()
        for document_data in documents_data:
            DriverDocument.objects.create(driver=instance, **document_data)
        
        return instance


class DriverAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['driver_id', 'is_available']

