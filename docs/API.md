# API Документация

## Обзор

REST API сайта салона красоты предоставляет доступ к данным об услугах, мастерах и позволяет создавать записи клиентов.

**Базовый URL:** `http://127.0.0.1:8000/api/`

**Формат данных:** JSON

**Аутентификация:** Не требуется (публичное API)

---

## Endpoints

### 1. Услуги

#### GET /api/services/

Получить список всех активных услуг.

**Ответ:**
```json
[
    {
        "id": 1,
        "name": "Женская стрижка",
        "description": "Стрижка с учётом типа волос и формы лица",
        "price": "1500.00",
        "duration": 60,
        "category": "hair",
        "category_display": "Парикмахерские услуги",
        "image": null
    }
]
```

#### GET /api/services/{id}/

Получить детали конкретной услуги.

---

### 2. Мастера

#### GET /api/masters/

Получить список всех активных мастеров с их услугами.

**Ответ:**
```json
[
    {
        "id": 1,
        "name": "Анна Петрова",
        "photo": null,
        "specialization": "Стилист-парикмахер",
        "experience": 8,
        "bio": "Анна — мастер с восьмилетним стажем...",
        "services": [
            {
                "id": 1,
                "name": "Женская стрижка",
                "price": "1500.00"
            }
        ],
        "is_active": true
    }
]
```

#### GET /api/masters/{id}/

Получить детали конкретного мастера.

#### GET /api/services/{service_id}/masters/

Получить мастеров, которые оказывают указанную услугу.

**Пример:** `/api/services/1/masters/` — мастера, делающие женские стрижки.

---

### 3. Записи (Appointments)

#### POST /api/appointments/

Создать новую запись клиента.

**Тело запроса:**
```json
{
    "client_name": "Иван Иванов",
    "client_phone": "+79001234567",
    "client_email": "ivan@example.com",
    "master": 1,
    "service": 2,
    "date": "2024-12-25",
    "time": "14:00",
    "comment": "Пожелания клиента"
}
```

**Обязательные поля:**
- `client_name` — имя клиента
- `client_phone` — телефон (формат: +7XXXXXXXXXX)
- `master` — ID мастера
- `service` — ID услуги
- `date` — дата (формат: YYYY-MM-DD)
- `time` — время (формат: HH:MM)

**Успешный ответ (201 Created):**
```json
{
    "success": true,
    "message": "Запись успешно создана! Мы свяжемся с вами для подтверждения.",
    "appointment_id": 1,
    "details": {
        "name": "Иван Иванов",
        "date": "25.12.2024",
        "time": "14:00",
        "master": "Анна Петрова",
        "service": "Женская стрижка"
    }
}
```

**Ошибка валидации (400 Bad Request):**
```json
{
    "success": false,
    "errors": {
        "date": ["Нельзя записаться на прошедшую дату"],
        "time": ["Запись возможна с 09:00 до 21:00"]
    }
}
```

---

### 4. Информация о салоне

#### GET /api/salon-info/

Получить информацию о салоне для главной страницы.

**Ответ:**
```json
{
    "id": 1,
    "name": "Салон красоты Elegance",
    "tagline": "Ваша красота — наша забота",
    "about_text": "Добро пожаловать...",
    "hero_image": null
}
```

---

### 5. Контакты

#### GET /api/contacts/

Получить контактную информацию салона.

**Ответ:**
```json
{
    "id": 1,
    "address": "г. Москва, ул. Примерная, д. 123",
    "phone": "+7 (495) 123-45-67",
    "email": "info@elegance-salon.ru",
    "working_hours": "Пн-Сб: 9:00-21:00, Вс: 10:00-18:00",
    "map_embed": "<iframe src='...'></iframe>",
    "vk_link": "https://vk.com/elegance_salon",
    "instagram_link": "",
    "telegram_link": "https://t.me/elegance_salon"
}
```

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | Успешный запрос |
| 201 | Ресурс создан |
| 400 | Ошибка валидации |
| 404 | Ресурс не найден |
| 500 | Внутренняя ошибка сервера |

---

## Примеры использования

### Python (requests)

```python
import requests

response = requests.get('http://127.0.0.1:8000/api/masters/')
masters = response.json()

data = {
    'client_name': 'Иван',
    'client_phone': '+79001234567',
    'master': 1,
    'service': 1,
    'date': '2024-12-25',
    'time': '14:00'
}
response = requests.post('http://127.0.0.1:8000/api/appointments/', json=data)
print(response.json())
```

