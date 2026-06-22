# 📚 Электронный дневник для колледжа
### Учебная практика ПМ.01 | Специальность 09.02.07

---

## 🚀 Запуск за 5 шагов

### 1. Установить Python
Скачать Python 3.10+ с https://python.org и установить.
При установке поставить галочку **"Add Python to PATH"**.

### 2. Установить зависимости
Открыть папку `college_diary` в терминале (правой кнопкой → "Открыть в терминале") и выполнить:

```
pip install -r requirements.txt
```

### 3. Создать базу данных

```
python manage.py migrate
```

### 4. Загрузить тестовые данные

```
python create_demo_data.py
```

### 5. Запустить сервер

```
python manage.py runserver
```

Открыть браузер: **http://127.0.0.1:8000**

---

## 👤 Тестовые аккаунты (пароль для всех: `pass123`)

| Логин     | Роль         | Описание                        |
|-----------|--------------|---------------------------------|
| admin     | Администратор| Полный доступ + /admin/         |
| selyutina | Учитель      | Численные методы                |
| kochetkov | Учитель      | Технология разработки ПО        |
| rassokha  | Учитель      | Разработка мобильных приложений |
| student1  | Ученик       | А.И Иванов 23-СПО-ИСиП-01       |
| student2  | Ученик       | Д.С. Смирнов 23-СПО-ИСиП-01     |
| student5  | Ученик       | М.В. Кузнецов 23-СПО-ИСиП-01    |

---

## 🗂 Структура проекта

```
college_diary/
├── manage.py               — точка входа Django
├── requirements.txt        — зависимости
├── create_demo_data.py     — скрипт тестовых данных
├── db.sqlite3              — база данных (создаётся автоматически)
│
├── config/                 — настройки проекта
│   ├── settings.py
│   └── urls.py
│
├── users/                  — приложение пользователей
│   ├── models.py           — модель User с ролями
│   ├── views.py
│   └── admin.py
│
├── journal/                — основное приложение
│   ├── models.py           — Subject, ClassRoom, Lesson, Grade
│   ├── views.py            — главная, расписание, журнал, оценки
│   ├── urls.py
│   └── templatetags/       — фильтр get_item
│
├── templates/              — HTML-шаблоны
│   ├── base.html
│   ├── registration/login.html
│   ├── journal/
│   └── users/
│
└── static/css/style.css    — стили
```

---

## ⚙️ Технологии

- **Backend:** Python 3.10+, Django 4.2
- **База данных:** SQLite (встроенная, не нужна установка)
- **Frontend:** HTML5 / CSS3 / JavaScript
- **Среда разработки:** Visual Studio Code
