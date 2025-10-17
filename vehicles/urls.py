from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, VehicleCategoryViewSet, VehicleSubCategoryViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'categories', VehicleCategoryViewSet)
router.register(r'sub-categories', VehicleSubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
