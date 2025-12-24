from django.contrib import admin
from .models import Service, Master, Appointment, Contact, SalonInfo

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = ['name', 'category', 'price', 'duration', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']
    fieldsets = [
        ('Основная информация', {
            'fields': ['name', 'description', 'category']
        }),
        ('Цена и время', {
            'fields': ['price', 'duration']
        }),
        ('Медиа', {
            'fields': ['image'],
            'classes': ['collapse']
        }),
        ('Статус', {
            'fields': ['is_active']
        }),
    ]

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):

    list_display = ['name', 'specialization', 'experience', 'is_active']
    list_filter = ['is_active', 'specialization']
    search_fields = ['name', 'specialization', 'bio']
    filter_horizontal = ['services']

    fieldsets = [
        ('Основная информация', {
            'fields': ['name', 'specialization', 'experience']
        }),
        ('Описание', {
            'fields': ['bio']
        }),
        ('Фото', {
            'fields': ['photo'],
            'classes': ['collapse']
        }),
        ('Услуги', {
            'fields': ['services'],
            'description': 'Выберите услуги, которые оказывает мастер'
        }),
        ('Статус', {
            'fields': ['is_active']
        }),
    ]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'client_name',
        'client_phone',
        'master',
        'service',
        'date',
        'time',
        'status',
        'created_at'
    ]

    list_filter = ['status', 'date', 'master', 'service']
    search_fields = ['client_name', 'client_phone', 'client_email']
    list_editable = ['status']
    ordering = ['-date', '-time']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'

    fieldsets = [
        ('Клиент', {
            'fields': ['client_name', 'client_phone', 'client_email']
        }),
        ('Запись', {
            'fields': ['master', 'service', 'date', 'time']
        }),
        ('Статус и комментарий', {
            'fields': ['status', 'comment']
        }),
        ('Служебная информация', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]

    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    @admin.action(description='Подтвердить выбранные записи')
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'Подтверждено записей: {updated}')

    @admin.action(description='Отметить как выполненные')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'Выполнено записей: {updated}')

    @admin.action(description='Отменить выбранные записи')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'Отменено записей: {updated}')



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email']

    fieldsets = [
        ('Основные контакты', {
            'fields': ['address', 'phone', 'email', 'working_hours']
        }),
        ('Карта', {
            'fields': ['map_embed'],
            'description': 'Вставьте HTML-код карты Яндекс или Google Maps'
        }),
        ('Социальные сети', {
            'fields': ['vk_link', 'instagram_link', 'telegram_link'],
            'classes': ['collapse']
        }),
    ]

@admin.register(SalonInfo)
class SalonInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline']

    fieldsets = [
        ('Основная информация', {
            'fields': ['name', 'tagline']
        }),
        ('О салоне', {
            'fields': ['about_text']
        }),
        ('Главное изображение', {
            'fields': ['hero_image'],
            'description': 'Рекомендуемый размер: 1920x1080 пикселей'
        }),
    ]

admin.site.site_header = 'Салон красоты - Админ-панель'
admin.site.site_title = 'Админ-панель салона'
admin.site.index_title = 'Управление салоном'

