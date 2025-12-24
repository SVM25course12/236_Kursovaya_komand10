from django.db import models
from django.core.validators import RegexValidator


class SalonInfo(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название салона',
        help_text='Например: "Салон красоты Elegance"'
    )
    tagline = models.CharField(
        max_length=300,
        verbose_name='Слоган',
        help_text='Краткий девиз салона',
        blank=True
    )
    about_text = models.TextField(
        verbose_name='О салоне',
        help_text='Развёрнутое описание салона для раздела "О нас"'
    )
    hero_image = models.ImageField(
        upload_to='salon/',
        verbose_name='Главное изображение',
        blank=True,
        null=True,
        help_text='Изображение для главного баннера (рекомендуется 1920x1080)'
    )

    class Meta:
        verbose_name = 'Информация о салоне'
        verbose_name_plural = 'Информация о салоне'

    def __str__(self):
        return self.name


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('hair', 'Парикмахерские услуги'),
        ('nails', 'Маникюр и педикюр'),
        ('face', 'Уход за лицом'),
        ('body', 'Уход за телом'),
        ('makeup', 'Макияж'),
        ('other', 'Другое'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Название услуги'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Подробное описание услуги'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена (руб.)',
        help_text='Цена услуги в рублях'
    )
    duration = models.PositiveIntegerField(
        verbose_name='Длительность (мин.)',
        default=60,
        help_text='Примерная длительность услуги в минутах'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория'
    )
    image = models.ImageField(
        upload_to='services/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Снимите галочку, чтобы скрыть услугу на сайте'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} - {self.price} руб.'


class Master(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='ФИО мастера'
    )
    photo = models.ImageField(
        upload_to='masters/',
        verbose_name='Фотография',
        blank=True,
        null=True
    )
    specialization = models.CharField(
        max_length=200,
        verbose_name='Специализация',
        help_text='Например: "Стилист-парикмахер", "Мастер маникюра"'
    )
    experience = models.PositiveIntegerField(
        verbose_name='Стаж (лет)',
        default=1,
        help_text='Опыт работы в годах'
    )
    bio = models.TextField(
        verbose_name='О мастере',
        blank=True,
        help_text='Краткая биография и достижения'
    )

    services = models.ManyToManyField(
        Service,
        related_name='masters',
        verbose_name='Услуги',
        blank=True,
        help_text='Выберите услуги, которые оказывает мастер'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Работает',
        help_text='Снимите галочку, если мастер временно не работает'
    )

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.specialization})'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?7?\d{10,11}$',
        message='Введите корректный номер телефона (например: +79001234567)'
    )

    client_name = models.CharField(
        max_length=200,
        verbose_name='Имя клиента'
    )
    client_phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        verbose_name='Телефон'
    )
    client_email = models.EmailField(
        verbose_name='Email',
        blank=True,
        help_text='Для отправки подтверждения (опционально)'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Мастер'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Услуга'
    )
    date = models.DateField(
        verbose_name='Дата'
    )
    time = models.TimeField(
        verbose_name='Время'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        help_text='Пожелания клиента'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.client_name} - {self.service.name} ({self.date} {self.time})'


class Contact(models.Model):
    address = models.CharField(
        max_length=300,
        verbose_name='Адрес',
        help_text='Полный адрес салона'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        verbose_name='Email'
    )
    working_hours = models.CharField(
        max_length=200,
        verbose_name='Режим работы',
        help_text='Например: "Пн-Сб: 9:00-21:00, Вс: выходной"'
    )
    map_embed = models.TextField(
        verbose_name='Код карты',
        blank=True,
        help_text='HTML-код для встраивания Яндекс.Карт или Google Maps'
    )

    vk_link = models.URLField(
        verbose_name='ВКонтакте',
        blank=True
    )
    instagram_link = models.URLField(
        verbose_name='Instagram',
        blank=True
    )
    telegram_link = models.URLField(
        verbose_name='Telegram',
        blank=True
    )

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'Контакты: {self.address}'

