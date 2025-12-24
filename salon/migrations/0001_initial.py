import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(help_text='Полный адрес салона', max_length=300, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('working_hours', models.CharField(help_text='Например: "Пн-Сб: 9:00-21:00, Вс: выходной"', max_length=200, verbose_name='Режим работы')),
                ('map_embed', models.TextField(blank=True, help_text='HTML-код для встраивания Яндекс.Карт или Google Maps', verbose_name='Код карты')),
                ('vk_link', models.URLField(blank=True, verbose_name='ВКонтакте')),
                ('instagram_link', models.URLField(blank=True, verbose_name='Instagram')),
                ('telegram_link', models.URLField(blank=True, verbose_name='Telegram')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='SalonInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Например: "Салон красоты Elegance"', max_length=200, verbose_name='Название салона')),
                ('tagline', models.CharField(blank=True, help_text='Краткий девиз салона', max_length=300, verbose_name='Слоган')),
                ('about_text', models.TextField(help_text='Развёрнутое описание салона для раздела "О нас"', verbose_name='О салоне')),
                ('hero_image', models.ImageField(blank=True, help_text='Изображение для главного баннера (рекомендуется 1920x1080)', null=True, upload_to='salon/', verbose_name='Главное изображение')),
            ],
            options={
                'verbose_name': 'Информация о салоне',
                'verbose_name_plural': 'Информация о салоне',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название услуги')),
                ('description', models.TextField(blank=True, help_text='Подробное описание услуги', verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, help_text='Цена услуги в рублях', max_digits=10, verbose_name='Цена (руб.)')),
                ('duration', models.PositiveIntegerField(default=60, help_text='Примерная длительность услуги в минутах', verbose_name='Длительность (мин.)')),
                ('category', models.CharField(choices=[('hair', 'Парикмахерские услуги'), ('nails', 'Маникюр и педикюр'), ('face', 'Уход за лицом'), ('body', 'Уход за телом'), ('makeup', 'Макияж'), ('other', 'Другое')], default='other', max_length=20, verbose_name='Категория')),
                ('image', models.ImageField(blank=True, null=True, upload_to='services/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть услугу на сайте', verbose_name='Активна')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['category', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ФИО мастера')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='masters/', verbose_name='Фотография')),
                ('specialization', models.CharField(help_text='Например: "Стилист-парикмахер", "Мастер маникюра"', max_length=200, verbose_name='Специализация')),
                ('experience', models.PositiveIntegerField(default=1, help_text='Опыт работы в годах', verbose_name='Стаж (лет)')),
                ('bio', models.TextField(blank=True, help_text='Краткая биография и достижения', verbose_name='О мастере')),
                ('is_active', models.BooleanField(default=True, help_text='Снимите галочку, если мастер временно не работает', verbose_name='Работает')),
                ('services', models.ManyToManyField(blank=True, help_text='Выберите услуги, которые оказывает мастер', related_name='masters', to='salon.service', verbose_name='Услуги')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=200, verbose_name='Имя клиента')),
                ('client_phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Введите корректный номер телефона (например: +79001234567)', regex='^\\+?7?\\d{10,11}$')], verbose_name='Телефон')),
                ('client_email', models.EmailField(blank=True, help_text='Для отправки подтверждения (опционально)', max_length=254, verbose_name='Email')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('confirmed', 'Подтверждена'), ('completed', 'Выполнена'), ('cancelled', 'Отменена')], default='new', max_length=20, verbose_name='Статус')),
                ('comment', models.TextField(blank=True, help_text='Пожелания клиента', verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='salon.master', verbose_name='Мастер')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='salon.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
                'ordering': ['-date', '-time'],
            },
        ),
    ]
