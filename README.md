# Сайт салона красоты Elegance

## Описание проекта

Учебный проект сайта салона красоты с онлайн-записью. Реализован как одностраничный лендинг с интерактивной прокруткой между секциями.

### Основные возможности

- **Главная страница** с информацией о салоне
- **Каталог услуг** с ценами и категориями
- **Страница мастеров** с портфолио
- **Онлайн-запись** через форму
- **Контакты** с интерактивной картой
- **Админ-панель** для управления контентом

---

## Технологии

| Компонент | Технология |
|-----------|------------|
| Backend | Python 3.x, Django 4.2 |
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| База данных | SQLite |
| API | Django REST Framework |
| Навигация | Intersection Observer API, CSS Scroll Snap |

---

## Быстрый старт

### 1. Клонирование и установка

```bash
# Перейти в директорию проекта
cd spa_site

# Создать виртуальное окружение (если ещё нет)
python -m venv .venv

# Активировать виртуальное окружение
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
# Создать таблицы в базе данных
python manage.py migrate

# Загрузить демо-данные (услуги, мастера, контакты)
python manage.py loaddata initial_data

# Создать администратора
python manage.py createsuperuser
```

### 3. Запуск сервера

```bash
python manage.py runserver
```

Сайт будет доступен по адресу: https://salon-demo.ant1coder.me/

Админ-панель: https://salon-demo.ant1coder.me/admin

---

## Структура проекта

```
spa_site/
├── spa_site/               
│   ├── settings.py         
│   ├── urls.py             
│   └── wsgi.py             
│
├── salon/                 
│   ├── models.py           
│   ├── views.py            
│   ├── serializers.py     
│   ├── admin.py            
│   ├── urls.py             
│   └── fixtures/          
│       └── initial_data.json
│
├── templates/            
│   └── salon/
│       └── index.html     
│
├── static/               
│   ├── css/
│   │   └── style.css     
│   └── js/
│       ├── navigation.js  
│       └── booking.js     
│
├── docs/                
├── tests/            
├── requirements.txt       
├── db.sqlite3             
└── manage.py              
```

---

## Команда разработки

| Роль | Ответственность |
|------|-----------------|
| **Тимлид** | Архитектура, стек технологий, код-ревью |
| **Backend** | Django, API, авторизация, работа с БД |
| **Frontend** | HTML/CSS/JS, UI/UX, адаптивная вёрстка |
| **Базист** | Проектирование БД, оптимизация запросов |
| **Тех. писатель** | Документация, комментарии в коде |
| **Тестировщик** | Тест-кейсы, проверка функционала |

---
