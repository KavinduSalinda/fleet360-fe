from rest_framework import serializers
from .models import Booking, BookingAddOn, BookingReturn, BookingExtension, Location
from customers.models import Customer
from vehicles.models import Vehicle
from drivers.models import Driver


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'name', 'address']


class BookingAddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingAddOn
        fields = ['add_on_name', 'add_on_price']


class BookingSerializer(serializers.ModelSerializer):
    add_ons = BookingAddOnSerializer(many=True, required=False)
    pickup_location = LocationSerializer(read_only=True)
    dropoff_location = LocationSerializer(read_only=True)
    
    pickup_location_id = serializers.IntegerField(write_only=True)
    dropoff_location_id = serializers.IntegerField(write_only=True)
    customer_id = serializers.IntegerField(write_only=True)
    vehicle_id = serializers.IntegerField(write_only=True)
    driver_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'booking_date', 'return_date', 'pickup_location',
            'dropoff_location', 'starting_odometer_reading', 'is_return_to_same_location',
            'driving_type', 'no_of_passengers', 'fuel_responsibility', 'deposited_amount',
            'is_vat_applicable', 'insurance_type', 'insurance_value', 'discount_type',
            'discount', 'total_amount', 'status', 'add_ons', 'pickup_location_id',
            'dropoff_location_id', 'customer_id', 'vehicle_id', 'driver_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['booking_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        add_ons_data = validated_data.pop('add_ons', [])
        
        # Get related objects
        pickup_location = Location.objects.get(id=validated_data.pop('pickup_location_id'))
        dropoff_location = Location.objects.get(id=validated_data.pop('dropoff_location_id'))
        customer = Customer.objects.get(id=validated_data.pop('customer_id'))
        vehicle = Vehicle.objects.get(id=validated_data.pop('vehicle_id'))
        
        driver_id = validated_data.pop('driver_id', None)
        driver = None
        if driver_id:
            driver = Driver.objects.get(id=driver_id)
        
        booking = Booking.objects.create(
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            customer=customer,
            vehicle=vehicle,
            driver=driver,
            **validated_data
        )
        
        for add_on_data in add_ons_data:
            BookingAddOn.objects.create(booking=booking, **add_on_data)
        
        return booking


class BookingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingReturn
        fields = [
            'return_date', 'final_odometer_reading', 'is_damage',
            'damage_notes', 'refunded_deposit_amount', 'total_amount'
        ]


class BookingExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingExtension
        fields = [
            'original_return_date', 'extend_return_date',
            'no_of_extend_days', 'price'
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    customer_information = serializers.SerializerMethodField()
    vehicle_information = serializers.SerializerMethodField()
    booking_period = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    price_breakdown = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'customer_information', 'vehicle_information',
            'booking_period', 'location', 'price_breakdown', 'created_at', 'updated_at'
        ]
    
    def get_customer_information(self, obj):
        return {
            'customer_id': obj.customer.customer_id,
            'customer_first_name': obj.customer.first_name,
            'customer_last_name': obj.customer.last_name,
            'contact_number': obj.customer.contact_number,
            'nic': obj.customer.nic
        }
    
    def get_vehicle_information(self, obj):
        return {
            'vehicle_id': obj.vehicle.vehicle_id,
            'make': obj.vehicle.make,
            'model': obj.vehicle.model,
            'vehicle_type': obj.vehicle.sub_category.sub_category_name,
            'registration_number': obj.vehicle.registration_no
        }
    
    def get_booking_period(self, obj):
        duration = (obj.return_date - obj.booking_date).days
        return {
            'pickup_date': obj.booking_date,
            'return_date': obj.return_date,
            'duration': duration
        }
    
    def get_location(self, obj):
        return {
            'pickup_location': {
                'id': obj.pickup_location.location_id,
                'name': obj.pickup_location.name,
                'address': obj.pickup_location.address
            },
            'return_location': {
                'id': obj.dropoff_location.location_id,
                'name': obj.dropoff_location.name,
                'address': obj.dropoff_location.address
            }
        }
    
    def get_price_breakdown(self, obj):
        add_ons_total = sum(add_on.add_on_price for add_on in obj.add_ons.all())
        return {
            'base_rate': obj.vehicle.price_per_day,
            'add_ons': [
                {'name': add_on.add_on_name, 'price': add_on.add_on_price}
                for add_on in obj.add_ons.all()
            ],
            'Excess rate': obj.vehicle.excess_km_charge,
            'tax': obj.vehicle.vat_amount,
            'deposit': obj.deposited_amount,
            'discount': obj.discount or 0,
            'total_amount': obj.total_amount
        }
