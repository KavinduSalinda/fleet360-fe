from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Vehicle, VehicleCategory, VehicleSubCategory
from .serializers import (
    VehicleSerializer, VehicleStatusSerializer, 
    VehicleAvailabilitySerializer, VehicleCategorySerializer,
    VehicleSubCategorySerializer
)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Vehicle.objects.all()
        query = self.request.query_params.get('query', None)
        category = self.request.query_params.get('category', None)
        sub_category = self.request.query_params.get('sub_category', None)
        fuel_type = self.request.query_params.get('fuel_type', None)
        available = self.request.query_params.get('available', None)
        
        if query:
            queryset = queryset.filter(
                Q(vehicle_name__icontains=query) |
                Q(make__icontains=query) |
                Q(model__icontains=query) |
                Q(registration_no__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category__category_name__iexact=category)
        
        if sub_category:
            queryset = queryset.filter(sub_category__sub_category_name__iexact=sub_category)
        
        if fuel_type:
            queryset = queryset.filter(fuel_type__iexact=fuel_type)
        
        if available:
            if available.lower() == 'true':
                queryset = queryset.filter(is_undermaintanace=False, status='available')
            elif available.lower() == 'false':
                queryset = queryset.filter(Q(is_undermaintanace=True) | ~Q(status='available'))
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'data': serializer.data,
            'message': 'vehicle added successfully',
            'status': 'success',
            'code': 201
        }, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # get category and sub_category from data and change the key to category and sub_category
        category_id = data.pop('category_id', None)
        sub_category_id = data.pop('sub_category_id', None)

        if category_id is not None:
            try:
                category = VehicleCategory.objects.get(pk=category_id)
                data['category'] = category.pk  # let serializer accept PK
            except VehicleCategory.DoesNotExist:
                return Response({
                    'message': 'Invalid category_id',
                    'status': 'error',
                    'code': 400
                }, status=status.HTTP_400_BAD_REQUEST)

        if sub_category_id is not None:
            try:
                sub_category = VehicleSubCategory.objects.get(pk=sub_category_id)

                if sub_category.category != category:
                    return Response({
                        'message': 'Invalid sub_category_id',
                        'status': 'error',
                        'code': 400
                    }, status=status.HTTP_400_BAD_REQUEST)
            except VehicleSubCategory.DoesNotExist:
                return Response({
                    'message': 'Invalid sub_category_id',
                    'status': 'error',
                    'code': 400
                }, status=status.HTTP_400_BAD_REQUEST)

            data['sub_category'] = sub_category.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'data': serializer.data,
            'message': 'vehicle added successfully',
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
            'message': f'vehicle {instance.vehicle_id} update successfully',
            'status': 'success',
            'code': 200
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'code': 200,
            'message': f'vehicle {instance.vehicle_id} deleted successfully'
        })
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['message'] = 'User retrieved successfully'
            paginated_response.data['status'] = 'success'
            paginated_response.data['code'] = 200
            return paginated_response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Vehicles retrieved successfully',
            'status': 'success',
            'code': 200
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'data': serializer.data,
            'message': f'Vehicle {instance.vehicle_id} details retrieved successfully',
            'status': 'success',
            'code': 200
        })
    
    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        vehicle = self.get_object()
        serializer = VehicleStatusSerializer(vehicle, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'data': serializer.data,
            'message': f'Vehicle {vehicle.vehicle_id} availability updated successfully',
            'status': 'success',
            'code': 200
        })
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        vehicle = self.get_object()
        available_from = request.query_params.get('available_from', None)
        available_to = request.query_params.get('available_to', None)
        
        # This would need to be implemented with booking logic
        serializer = VehicleAvailabilitySerializer(vehicle)
        
        return Response({
            'data': serializer.data,
            'message': 'Vehicle availability details retrieved successfully',
            'status': 'success',
            'code': 200
        })


class VehicleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializer


class VehicleSubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleSubCategory.objects.all()
    serializer_class = VehicleSubCategorySerializer
