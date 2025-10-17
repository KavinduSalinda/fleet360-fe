from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
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
        
        return Response({
            'data': serializer.data,
            'message': 'Data added successfully.',
            'status': 'success',
            'code': 201
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'data': serializer.data,
            'message': 'Data updated successfully.',
            'status': 'success',
            'code': 200
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'code': 200,
            'message': 'Customer deleted successfully'
        })
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'pagination': {
                'current_page': 1,
                'total_pages': None,
                'total_items': None,
                'items_per_page': None,
                'has_next': None,
                'has_previous': None
            },
            'message': 'Data recieved successfully.',
            'status': 'success',
            'code': 200
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'data': serializer.data,
            'message': 'Data recieved successfully.',
            'status': 'success',
            'code': 200
        })
    
    @action(detail=True, methods=['get', 'patch'])
    def status(self, request, pk=None):
        customer = self.get_object()
        
        if request.method == 'GET':
            # Handle GET request - return customer status
            serializer = CustomerStatusSerializer(customer)
            return Response({
                'data': serializer.data,
                'message': 'Data recieved successfully.',
                'status': 'success',
                'code': 200
            })
        
        elif request.method == 'PATCH':
            # Handle PATCH request - update customer status
            serializer = CustomerStatusSerializer(customer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({
                'data': serializer.data,
                'message': 'Data updated successfully.',
                'status': 'success',
                'code': 200
            })
