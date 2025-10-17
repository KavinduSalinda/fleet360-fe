from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, LocationViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/locations/', LocationViewSet.as_view({'get': 'list'}), name='booking-locations'),
]
