from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from fleet360.responses import StandardResponse
from .models import Booking, BookingReturn, BookingExtension, Location
from .serializers import (
    BookingSerializer, BookingReturnSerializer, BookingExtensionSerializer,
    BookingDetailSerializer, LocationSerializer
)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Booking.objects.all()
        booking_id = self.request.query_params.get('booking_id', None)
        customer_id = self.request.query_params.get('customer_id', None)
        date = self.request.query_params.get('date', None)
        vehicle_id = self.request.query_params.get('vehicle_id', None)
        status_filter = self.request.query_params.get('status', None)
        
        if booking_id:
            queryset = queryset.filter(booking_id=booking_id)
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if date:
            queryset = queryset.filter(booking_date__date=date)
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        if status_filter:
            queryset = queryset.filter(status__iexact=status_filter)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        return StandardResponse(
            data=BookingSerializer(booking).data,
            message='Booking created successfully',
            code=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        pagination_data = self.paginator.get_custom_pagination_data()
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        
        return StandardResponse(
            data=serializer.data,
            message='Bookings retrieved successfully',
            code=status.HTTP_200_OK,
            pagination=pagination_data
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookingDetailSerializer(instance)
        
        return StandardResponse(
            data=serializer.data,
            message='Booking details retrieved successfully',
            code=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def returns(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_obj = serializer.save(booking=booking)
        
        return StandardResponse(
            data=serializer.data,
            message='Booking returned successfully',
            code=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def extensions(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingExtensionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        extension = serializer.save(booking=booking)
        
        return StandardResponse(
            data=serializer.data,
            message='Booking extended successfully',
            code=status.HTTP_200_OK
        )


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return StandardResponse(
            data={'locations': serializer.data},
            message='Locations retrieved successfully',
            code=status.HTTP_200_OK
        )
