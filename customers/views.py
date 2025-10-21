from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from fleet360.responses import StandardResponse
from .models import Customer
from .serializers import CustomerSerializer, CustomerStatusSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Customer.objects.all()
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
            message='Customer created successfully',
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
            message='Customer updated successfully',
            code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return StandardResponse(
            message='Customer deleted successfully',
            code=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return StandardResponse(
            data=serializer.data,
            message='Customers retrieved successfully',
            code=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return StandardResponse(
            data=serializer.data,
            message='Customer details retrieved successfully',
            code=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get', 'patch'])
    def status(self, request, pk=None):
        customer = self.get_object()
        
        if request.method == 'GET':
            # Handle GET request - return customer status
            serializer = CustomerStatusSerializer(customer)
            return StandardResponse(
                data=serializer.data,
                message='Customer status retrieved successfully',
                code=status.HTTP_200_OK
            )
        
        elif request.method == 'PATCH':
            # Handle PATCH request - update customer status
            serializer = CustomerStatusSerializer(customer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return StandardResponse(
                data=serializer.data,
                message='Customer status updated successfully',
                code=status.HTTP_200_OK
            )
