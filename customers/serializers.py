from rest_framework import serializers
from .models import Customer, CustomerDocument


class CustomerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDocument
        fields = ['document_name', 'document_hash', 'document_url']


class CustomerSerializer(serializers.ModelSerializer):
    documents = CustomerDocumentSerializer(many=True, required=False)
    
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'first_name', 'last_name', 'user_name', 'email',
            'contact_number', 'address', 'nic', 'passport_number', 'nationality',
            'country', 'driving_licence_number', 'status', 'is_active',
            'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['customer_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        documents_data = validated_data.pop('documents', [])
        customer = Customer.objects.create(**validated_data)
        
        for document_data in documents_data:
            CustomerDocument.objects.create(customer=customer, **document_data)
        
        return customer
    
    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', [])
        
        # Update customer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update documents
        instance.documents.all().delete()
        for document_data in documents_data:
            CustomerDocument.objects.create(customer=instance, **document_data)
        
        return instance


class CustomerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'status', 'updated_at']

