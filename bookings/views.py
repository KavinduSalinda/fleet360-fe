from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
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
        
        return Response({
            'data': BookingSerializer(booking).data,
            'message': 'Booking placed successfully',
            'status': 'success',
            'code': 201
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['message'] = 'Booking categories retrieved successfully'
            paginated_response.data['status'] = 'success'
            paginated_response.data['code'] = 200
            return paginated_response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Bookings retrieved successfully',
            'status': 'success',
            'code': 200
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BookingDetailSerializer(instance)
        
        return Response({
            'data': serializer.data,
            'message': 'Booking details recieved successfully',
            'status': 'success',
            'code': 200
        })
    
    @action(detail=True, methods=['post'])
    def returns(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_obj = serializer.save(booking=booking)
        
        return Response({
            'data': serializer.data,
            'status': 'success',
            'code': 200,
            'message': 'Booking has been returned successfully'
        })
    
    @action(detail=True, methods=['post'])
    def extensions(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingExtensionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        extension = serializer.save(booking=booking)
        
        return Response({
            'data': serializer.data,
            'status': 'success',
            'code': 200,
            'message': 'Booking extended successfully'
        })


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'data': {'locations': serializer.data},
            'status': 'success',
            'code': 200,
            'message': 'Locations retrieved successfully'
        })
