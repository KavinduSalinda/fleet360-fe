from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from fleet360.responses import StandardResponse
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
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
        
    #     return Response({
    #         'data': serializer.data,
    #         'message': 'vehicle added successfully',
    #         'status': 'success',
    #         'code': 201
    #     }, status=status.HTTP_201_CREATED)

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
                return StandardResponse(
                    message='Invalid category_id',
                    code=status.HTTP_400_BAD_REQUEST
                )

        if sub_category_id is not None:
            try:
                sub_category = VehicleSubCategory.objects.get(pk=sub_category_id)

                if sub_category.category != category:
                    return StandardResponse(
                        message='Sub-category does not belong to the specified category',
                        code=status.HTTP_400_BAD_REQUEST
                    )
            except VehicleSubCategory.DoesNotExist:
                return StandardResponse(
                    message='Invalid sub_category_id',
                    code=status.HTTP_400_BAD_REQUEST
                )

            data['sub_category'] = sub_category.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return StandardResponse(
            data=serializer.data,
            message='Vehicle created successfully',
            code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        
        data = request.data.copy()
        # get category and sub_category from data and change the key to category and sub_category
        category_id = data.pop('category_id', None)
        sub_category_id = data.pop('sub_category_id', None)
        
        category = None  # Initialize category variable

        if category_id is not None:
            try:
                category = VehicleCategory.objects.get(pk=category_id)
                data['category'] = category.pk  # let serializer accept PK
            except VehicleCategory.DoesNotExist:
                return StandardResponse(
                    message='Invalid category_id',
                    code=status.HTTP_400_BAD_REQUEST
                )

        if sub_category_id is not None:
            try:
                sub_category = VehicleSubCategory.objects.get(pk=sub_category_id)

                # Only validate if category was provided in this request
                if category is not None and sub_category.category != category:
                    return StandardResponse(
                        message='Sub-category does not belong to the specified category',
                        code=status.HTTP_400_BAD_REQUEST
                    )
            except VehicleSubCategory.DoesNotExist:
                return StandardResponse(
                    message='Invalid sub_category_id',
                    code=status.HTTP_400_BAD_REQUEST
                )

            data['sub_category'] = sub_category.pk

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Use the modified data instead of request.data
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return StandardResponse(
            data=serializer.data,
            message=f'Vehicle {instance.vehicle_id} updated successfully',
            code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return StandardResponse(
            message=f'Vehicle {instance.vehicle_id} deleted successfully',
            code=status.HTTP_200_OK
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
            message='Vehicles retrieved successfully',
            code=status.HTTP_200_OK,
            pagination=pagination_data
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return StandardResponse(
            data=serializer.data,
            message=f'Vehicle {instance.vehicle_id} details retrieved successfully',
            code=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['patch', 'get'])
    def status(self, request, pk=None):

        method = request.method

        if method == 'PATCH':
            vehicle = self.get_object()
            serializer = VehicleStatusSerializer(vehicle, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return StandardResponse(
                data=serializer.data,
                message=f'Vehicle {vehicle.vehicle_id} status updated successfully',
                code=status.HTTP_200_OK
            )
        
        if method == 'GET':
            vehicle = self.get_object()
            available_from = request.query_params.get('available_from', None)
            available_to = request.query_params.get('available_to', None)
            
            if not available_from and not available_to:
                return StandardResponse(
                    message='Available from and available to are required',
                    code=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = VehicleAvailabilitySerializer(vehicle)
            
            return StandardResponse(
                data=serializer.data,
                message='Vehicle availability details retrieved successfully',
                code=status.HTTP_200_OK
            )
        

        
        
    


class VehicleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleCategory.objects.all()
    serializer_class = VehicleCategorySerializer


class VehicleSubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleSubCategory.objects.all()
    serializer_class = VehicleSubCategorySerializer
