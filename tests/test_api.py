from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta

from salon.models import Service, Master, Appointment, Contact, SalonInfo


class ServiceAPITest(APITestCase):
    def setUp(self):
        self.service1 = Service.objects.create(
            name='Стрижка',
            price=Decimal('1500.00'),
            duration=60,
            category='hair',
            is_active=True
        )
        self.service2 = Service.objects.create(
            name='Маникюр',
            price=Decimal('1000.00'),
            duration=45,
            category='nails',
            is_active=True
        )
        self.inactive_service = Service.objects.create(
            name='Скрытая услуга',
            price=Decimal('500.00'),
            duration=30,
            category='other',
            is_active=False
        )

    def test_get_services_list(self):
        url = '/api/services/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_service_detail(self):
        url = f'/api/services/{self.service1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Стрижка')
        self.assertEqual(response.data['category'], 'hair')

    def test_inactive_service_not_in_list(self):
        url = '/api/services/'
        response = self.client.get(url)

        names = [s['name'] for s in response.data]
        self.assertNotIn('Скрытая услуга', names)


class MasterAPITest(APITestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Тестовая услуга',
            price=Decimal('1000.00'),
            duration=30,
            category='hair'
        )

        self.master = Master.objects.create(
            name='Анна Тестова',
            specialization='Стилист',
            experience=5,
            is_active=True
        )
        self.master.services.add(self.service)

        self.inactive_master = Master.objects.create(
            name='Неактивный мастер',
            specialization='Тест',
            experience=1,
            is_active=False
        )

    def test_get_masters_list(self):
        url = '/api/masters/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Анна Тестова')

    def test_master_includes_services(self):
        url = f'/api/masters/{self.master.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['services']), 1)
        self.assertEqual(response.data['services'][0]['name'], 'Тестовая услуга')

    def test_get_masters_for_service(self):
        url = f'/api/services/{self.service.id}/masters/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Анна Тестова')


class AppointmentAPITest(APITestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Услуга для записи',
            price=Decimal('2000.00'),
            duration=60,
            category='nails'
        )

        self.master = Master.objects.create(
            name='Мастер для записи',
            specialization='Специалист',
            experience=3
        )
        self.master.services.add(self.service)
        self.future_date = date.today() + timedelta(days=7)

    def test_create_appointment_success(self):
        url = '/api/appointments/'
        data = {
            'client_name': 'Иван Тестов',
            'client_phone': '+79001234567',
            'client_email': 'test@example.com',
            'master': self.master.id,
            'service': self.service.id,
            'date': self.future_date.strftime('%Y-%m-%d'),
            'time': '14:00',
            'comment': 'Тестовая запись'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('appointment_id', response.data)

        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.client_name, 'Иван Тестов')
        self.assertEqual(appointment.status, 'new')

    def test_create_appointment_past_date(self):
        url = '/api/appointments/'
        past_date = date.today() - timedelta(days=1)

        data = {
            'client_name': 'Иван',
            'client_phone': '+79001234567',
            'master': self.master.id,
            'service': self.service.id,
            'date': past_date.strftime('%Y-%m-%d'),
            'time': '14:00'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_create_appointment_missing_fields(self):
        url = '/api/appointments/'
        data = {
            'client_name': 'Иван'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ContactAPITest(APITestCase):
    def test_get_contacts_empty(self):
        url = '/api/contacts/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_get_contacts_filled(self):
        Contact.objects.create(
            address='г. Тест',
            phone='+7 (123) 456-78-90',
            email='test@test.ru',
            working_hours='Пн-Пт: 9-18'
        )

        url = '/api/contacts/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+7 (123) 456-78-90')


class SalonInfoAPITest(APITestCase):
    def test_get_salon_info_empty(self):
        url = '/api/salon-info/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_get_salon_info_filled(self):
        SalonInfo.objects.create(
            name='Тестовый салон',
            tagline='Лучший салон',
            about_text='Описание'
        )

        url = '/api/salon-info/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Тестовый салон')

