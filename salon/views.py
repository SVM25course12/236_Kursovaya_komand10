from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from .models import Service, Master, Appointment, Contact, SalonInfo
from .serializers import (
    ServiceSerializer,
    MasterSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
    ContactSerializer,
    SalonInfoSerializer
)

class IndexView(TemplateView):
    template_name = 'salon/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon_info'] = SalonInfo.objects.first()
        context['services'] = Service.objects.filter(is_active=True)

        services_by_category = {}
        for service in context['services']:
            category = service.get_category_display()
            if category not in services_by_category:
                services_by_category[category] = []
            services_by_category[category].append(service)
        context['services_by_category'] = services_by_category

        context['masters'] = Master.objects.filter(is_active=True).prefetch_related('services')
        context['contacts'] = Contact.objects.first()

        return context

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]  # Доступно всем без авторизации


class MasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Master.objects.filter(is_active=True).prefetch_related('services')
    serializer_class = MasterSerializer
    permission_classes = [AllowAny]


class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            appointment = serializer.save()
            return Response({
                'success': True,
                'message': 'Запись успешно создана! Мы свяжемся с вами для подтверждения.',
                'appointment_id': appointment.id,
                'details': {
                    'name': appointment.client_name,
                    'date': appointment.date.strftime('%d.%m.%Y'),
                    'time': appointment.time.strftime('%H:%M'),
                    'master': appointment.master.name,
                    'service': appointment.service.name
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_contacts(request):
    contact = Contact.objects.first()
    if contact:
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
    return Response({})


@api_view(['GET'])
def get_salon_info(request):
    salon_info = SalonInfo.objects.first()
    if salon_info:
        serializer = SalonInfoSerializer(salon_info)
        return Response(serializer.data)
    return Response({})


@api_view(['GET'])
def get_masters_for_service(request, service_id):
    masters = Master.objects.filter(
        is_active=True,
        services__id=service_id
    ).distinct()

    serializer = MasterSerializer(masters, many=True)
    return Response(serializer.data)

