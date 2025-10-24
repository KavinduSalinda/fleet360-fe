from rest_framework import serializers
from .models import Vehicle, VehicleDocument, VehicleImage, VehicleCategory, VehicleSubCategory
from bookings.models import Booking
from django.db.models import Q
from datetime import date, timedelta


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
    is_available_for_dates = serializers.SerializerMethodField()
    available_in_days = serializers.SerializerMethodField()
    
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
            'is_available_for_dates', 'available_in_days',
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
    
    def parse_custom_date(self, date_str):
        """Parse custom date format (YYYYMMDD) to standard date format"""
        if date_str and len(date_str) == 8:
            try:
                year = int(date_str[:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])
                return date(year, month, day)
            except ValueError:
                return None
        return None
    
    def get_is_available_for_dates(self, obj):
        """Check if vehicle is available for the requested date range"""
        # Get date parameters from context (passed from view)
        pickup_date = self.context.get('pickup_date')
        dropoff_date = self.context.get('dropoff_date')
        
        if not pickup_date or not dropoff_date:
            return True  # If no dates provided, assume available
        
        parsed_pickup = self.parse_custom_date(pickup_date)
        parsed_dropoff = self.parse_custom_date(dropoff_date)
        
        if not parsed_pickup or not parsed_dropoff:
            return True  # If date parsing fails, assume available
        
        # Check if vehicle has any confirmed/ongoing bookings that overlap with requested dates
        overlapping_bookings = Booking.objects.filter(
            Q(vehicle=obj),
            Q(status__in=['confirmed', 'ongoing']),
            Q(booking_date__date__lte=parsed_dropoff) & Q(return_date__date__gte=parsed_pickup)
        ).exists()
        
        return not overlapping_bookings
    
    def get_available_in_days(self, obj):
        """Calculate how many days until vehicle is available"""
        pickup_date = self.context.get('pickup_date')
        dropoff_date = self.context.get('dropoff_date')
        
        if not pickup_date or not dropoff_date:
            return None
        
        parsed_pickup = self.parse_custom_date(pickup_date)
        parsed_dropoff = self.parse_custom_date(dropoff_date)
        
        if not parsed_pickup or not parsed_dropoff:
            return None
        
        # If vehicle is available for the requested dates, return None
        if self.get_is_available_for_dates(obj):
            return None
        
        # Find the next available date after the requested dropoff date
        overlapping_bookings = Booking.objects.filter(
            Q(vehicle=obj),
            Q(status__in=['confirmed', 'ongoing']),
            Q(return_date__date__gte=parsed_dropoff)
        ).order_by('return_date')
        
        if overlapping_bookings.exists():
            # Get the latest return date from overlapping bookings
            latest_return_date = overlapping_bookings.last().return_date.date()
            days_until_available = (latest_return_date - parsed_dropoff).days + 1
            return max(0, days_until_available)
        
        return None


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
