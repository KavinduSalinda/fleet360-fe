from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from fleet360.responses import StandardResponse
from .models import Driver
from .serializers import DriverSerializer, DriverAvailabilitySerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Driver.objects.all()
        query = self.request.query_params.get('query', None)
        
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(contact_number__icontains=query) |
                Q(nic__icontains=query)
            )
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return StandardResponse(
            data=serializer.data,
            message='Driver created successfully',
            code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return StandardResponse(
            data=serializer.data,
            message='Driver updated successfully',
            code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return StandardResponse(
            message='Driver deleted successfully',
            code=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['message'] = 'Drivers received successfully'
            paginated_response.data['status'] = 'success'
            paginated_response.data['code'] = 200
            return paginated_response
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(
            data=serializer.data,
            message='Drivers retrieved successfully',
            code=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return StandardResponse(
            data=serializer.data,
            message='Driver details retrieved successfully',
            code=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        driver = self.get_object()
        available_from = request.query_params.get('available_from', None)
        available_to = request.query_params.get('available_to', None)
        
        serializer = DriverAvailabilitySerializer(driver)
        
        return StandardResponse(
            data=serializer.data,
            message='Driver status retrieved successfully',
            code=status.HTTP_200_OK
        )
