from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    IndexView,
    ServiceViewSet,
    MasterViewSet,
    AppointmentCreateView,
    get_contacts,
    get_salon_info,
    get_masters_for_service
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'masters', MasterViewSet, basename='master')


urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('api/appointments/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('api/contacts/', get_contacts, name='contacts'),
    path('api/salon-info/', get_salon_info, name='salon-info'),
    path('api/services/<int:service_id>/masters/', get_masters_for_service, name='service-masters'),
]

