from rest_framework import serializers
from .models import Service, Master, Appointment, Contact, SalonInfo
from django.utils import timezone


class ServiceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )

    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration',
            'category',
            'category_display',
            'image'
        ]


class MasterSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Master
        fields = [
            'id',
            'name',
            'photo',
            'specialization',
            'experience',
            'bio',
            'services',
            'is_active'
        ]


class MasterShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ['id', 'name', 'specialization']


class AppointmentSerializer(serializers.ModelSerializer):
    master_details = MasterShortSerializer(source='master', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            'id',
            'client_name',
            'client_phone',
            'client_email',
            'master',
            'master_details',
            'service',
            'service_details',
            'date',
            'time',
            'status',
            'status_display',
            'comment',
            'created_at'
        ]

        read_only_fields = ['status', 'created_at']

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Нельзя записаться на прошедшую дату'
            )
        return value

    def validate_time(self, value):
        from datetime import time

        opening_time = time(9, 0)   # 9:00
        closing_time = time(21, 0)  # 21:00

        if value < opening_time or value >= closing_time:
            raise serializers.ValidationError(
                f'Запись возможна с {opening_time.strftime("%H:%M")} до {closing_time.strftime("%H:%M")}'
            )
        return value

    def validate(self, data):
        master = data.get('master')
        service = data.get('service')

        if master and service:
            if not master.services.filter(id=service.id).exists():
                raise serializers.ValidationError({
                    'service': f'Мастер {master.name} не оказывает услугу "{service.name}"'
                })

        return data


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'client_name',
            'client_phone',
            'client_email',
            'master',
            'service',
            'date',
            'time',
            'comment'
        ]

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Нельзя записаться на прошедшую дату'
            )
        return value


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'address',
            'phone',
            'email',
            'working_hours',
            'map_embed',
            'vk_link',
            'instagram_link',
            'telegram_link'
        ]


class SalonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonInfo
        fields = [
            'id',
            'name',
            'tagline',
            'about_text',
            'hero_image'
        ]

