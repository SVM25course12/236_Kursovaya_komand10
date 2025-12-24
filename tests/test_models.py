from django.test import TestCase
from decimal import Decimal
from salon.models import Service, Master, Appointment, Contact, SalonInfo
from datetime import date, time


class ServiceModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Тестовая стрижка',
            description='Описание услуги',
            price=Decimal('1500.00'),
            duration=60,
            category='hair',
            is_active=True
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, 'Тестовая стрижка')
        self.assertEqual(self.service.price, Decimal('1500.00'))
        self.assertTrue(self.service.is_active)

    def test_service_str(self):
        expected = 'Тестовая стрижка - 1500.00 руб.'
        self.assertEqual(str(self.service), expected)

    def test_service_category_display(self):
        self.assertEqual(
            self.service.get_category_display(),
            'Парикмахерские услуги'
        )


class MasterModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Тестовая услуга',
            price=Decimal('1000.00'),
            duration=30,
            category='hair'
        )

        self.master = Master.objects.create(
            name='Тест Мастеров',
            specialization='Тестовый мастер',
            experience=5,
            bio='Биография',
            is_active=True
        )
        self.master.services.add(self.service)

    def test_master_creation(self):
        self.assertEqual(self.master.name, 'Тест Мастеров')
        self.assertEqual(self.master.experience, 5)
        self.assertTrue(self.master.is_active)

    def test_master_str(self):
        expected = 'Тест Мастеров (Тестовый мастер)'
        self.assertEqual(str(self.master), expected)

    def test_master_services_relation(self):
        self.assertEqual(self.master.services.count(), 1)
        self.assertIn(self.service, self.master.services.all())


class AppointmentModelTest(TestCase):
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

        self.appointment = Appointment.objects.create(
            client_name='Клиент Тестов',
            client_phone='+79001234567',
            client_email='test@example.com',
            master=self.master,
            service=self.service,
            date=date(2025, 12, 25),
            time=time(14, 0),
            status='new',
            comment='Тестовый комментарий'
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.client_name, 'Клиент Тестов')
        self.assertEqual(self.appointment.client_phone, '+79001234567')
        self.assertEqual(self.appointment.status, 'new')

    def test_appointment_str(self):
        self.assertIn('Клиент Тестов', str(self.appointment))
        self.assertIn('Услуга для записи', str(self.appointment))

    def test_appointment_relations(self):
        self.assertEqual(self.appointment.master, self.master)
        self.assertEqual(self.appointment.service, self.service)

    def test_appointment_status_choices(self):
        self.appointment.status = 'confirmed'
        self.appointment.save()
        self.assertEqual(
            self.appointment.get_status_display(),
            'Подтверждена'
        )


class ContactModelTest(TestCase):
    def test_contact_creation(self):
        contact = Contact.objects.create(
            address='г. Тест, ул. Тестовая, д. 1',
            phone='+7 (123) 456-78-90',
            email='test@salon.ru',
            working_hours='Пн-Пт: 9-18'
        )

        self.assertEqual(contact.phone, '+7 (123) 456-78-90')
        self.assertIn('Тест', str(contact))


class SalonInfoModelTest(TestCase):
    def test_salon_info_creation(self):
        info = SalonInfo.objects.create(
            name='Тестовый салон',
            tagline='Лучший салон',
            about_text='Описание салона'
        )

        self.assertEqual(info.name, 'Тестовый салон')
        self.assertEqual(str(info), 'Тестовый салон')

