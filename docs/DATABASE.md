# Структура базы данных

## Обзор

База данных использует SQLite — встроенную СУБД Python. Для учебного проекта это оптимальный выбор:
- Не требует отдельной установки
- Хранится в одном файле (db.sqlite3)
- Полностью совместима с Django ORM

---

## ER-диаграмма (Entity-Relationship)

```
┌─────────────────┐       ┌─────────────────┐
│   SalonInfo     │       │     Contact     │
│─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │
│ name            │       │ address         │
│ tagline         │       │ phone           │
│ about_text      │       │ email           │
│ hero_image      │       │ working_hours   │
└─────────────────┘       │ map_embed       │
                          │ vk_link         │
                          │ instagram_link  │
                          │ telegram_link   │
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Service      │◄──────│  MasterService  │──────►│     Master      │
│─────────────────│  M:N  │─────────────────│  M:N  │─────────────────│
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ name            │       │ master_id (FK)  │       │ name            │
│ description     │       │ service_id (FK) │       │ photo           │
│ price           │       └─────────────────┘       │ specialization  │
│ duration        │                                 │ experience      │
│ category        │                                 │ bio             │
│ image           │                                 │ is_active       │
│ is_active       │                                 └────────┬────────┘
└────────┬────────┘                                          │
         │                                                   │
         │ 1:N                                          1:N  │
         │                                                   │
         │         ┌─────────────────────────┐               │
         └────────►│      Appointment        │◄──────────────┘
                   │─────────────────────────│
                   │ id (PK)                 │
                   │ client_name             │
                   │ client_phone            │
                   │ client_email            │
                   │ master_id (FK)          │
                   │ service_id (FK)         │
                   │ date                    │
                   │ time                    │
                   │ status                  │
                   │ comment                 │
                   │ created_at              │
                   └─────────────────────────┘
```

---

## Описание таблиц

### 1. SalonInfo (Информация о салоне)

Хранит основные данные салона для главной страницы. Таблица-синглтон (одна запись).

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| name | VARCHAR(200) | Название салона |
| tagline | VARCHAR(300) | Слоган/девиз |
| about_text | TEXT | Текст "О нас" |
| hero_image | VARCHAR (путь) | Главное изображение |

---

### 2. Contact (Контакты)

Контактная информация салона. Таблица-синглтон.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| address | VARCHAR(300) | Адрес |
| phone | VARCHAR(20) | Телефон |
| email | VARCHAR(254) | Email |
| working_hours | VARCHAR(200) | Режим работы |
| map_embed | TEXT | HTML-код карты |
| vk_link | VARCHAR(200) | Ссылка на VK |
| instagram_link | VARCHAR(200) | Ссылка на Instagram |
| telegram_link | VARCHAR(200) | Ссылка на Telegram |

---

### 3. Service (Услуги)

Каталог услуг салона.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| name | VARCHAR(200) | Название услуги |
| description | TEXT | Описание |
| price | DECIMAL(10,2) | Цена в рублях |
| duration | INTEGER | Длительность (мин) |
| category | VARCHAR(20) | Категория (hair/nails/face/body/makeup/other) |
| image | VARCHAR (путь) | Изображение |
| is_active | BOOLEAN | Активна ли услуга |

**Категории услуг:**
на- `hair` — Парикмахерские услуги
- `nails` — Маникюр и педикюр
- `face` — Уход за лицом
- `body` — Уход за телом
- `makeup` — Макияж
- `other` — Другое

---

### 4. Master (Мастера)

Информация о мастерах салона.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| name | VARCHAR(200) | ФИО мастера |
| photo | VARCHAR (путь) | Фотография |
| specialization | VARCHAR(200) | Специализация |
| experience | INTEGER | Стаж (лет) |
| bio | TEXT | Биография |
| is_active | BOOLEAN | Работает ли сейчас |

**Связь с услугами:** Many-to-Many через таблицу `salon_master_services`

---

### 5. Appointment (Записи)

Записи клиентов на услуги.

| Поле | Тип | Описание |
|------|-----|----------|
| id | INTEGER (PK) | Первичный ключ |
| client_name | VARCHAR(200) | Имя клиента |
| client_phone | VARCHAR(15) | Телефон |
| client_email | VARCHAR(254) | Email (опционально) |
| master_id | INTEGER (FK) | Ссылка на мастера |
| service_id | INTEGER (FK) | Ссылка на услугу |
| date | DATE | Дата записи |
| time | TIME | Время записи |
| status | VARCHAR(20) | Статус записи |
| comment | TEXT | Комментарий клиента |
| created_at | DATETIME | Дата создания |

**Статусы записи:**
- `new` — Новая (только создана)
- `confirmed` — Подтверждена администратором
- `completed` — Выполнена
- `cancelled` — Отменена

---

## Связи между таблицами

| Связь | Тип | Описание |
|-------|-----|----------|
| Master ↔ Service | M:N | Мастер может оказывать несколько услуг, услугу могут оказывать несколько мастеров |
| Appointment → Master | N:1 | Запись принадлежит одному мастеру |
| Appointment → Service | N:1 | Запись на одну услугу |

---

## SQL-запросы (примеры)

### Получить все услуги мастера

```sql
SELECT s.name, s.price
FROM salon_service s
JOIN salon_master_services ms ON s.id = ms.service_id
WHERE ms.master_id = 1;
```

### Получить записи на сегодня

```sql
SELECT a.client_name, a.time, m.name as master, s.name as service
FROM salon_appointment a
JOIN salon_master m ON a.master_id = m.id
JOIN salon_service s ON a.service_id = s.id
WHERE a.date = DATE('now')
ORDER BY a.time;
```

### Подсчёт записей по статусам

```sql
SELECT status, COUNT(*) as count
FROM salon_appointment
GROUP BY status;
```

---

## Миграции

Django автоматически управляет схемой БД через миграции.

```bash
# Создать миграции после изменения моделей
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Посмотреть SQL-код миграции
python manage.py sqlmigrate salon 0001
```

