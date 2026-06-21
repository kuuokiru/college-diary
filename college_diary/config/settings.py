# ======================================================
# НАСТРОЙКИ ПРОЕКТА — Электронный дневник ИМСИТ
# Здесь хранятся все основные настройки приложения
# ======================================================

from pathlib import Path

# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (не менять в продакшне!)
SECRET_KEY = 'django-insecure-college-diary-imsit-2025'

# Режим отладки (True = показывает ошибки подробно)
DEBUG = True
ALLOWED_HOSTS = ['*']

# Список установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',       # Панель администратора
    'django.contrib.auth',        # Аутентификация
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # Сессии пользователей
    'django.contrib.messages',    # Уведомления
    'django.contrib.staticfiles', # Статические файлы (CSS, JS)
    'users',                      # Наше приложение: пользователи
    'journal',                    # Наше приложение: журнал и оценки
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Главный файл маршрутов (URLs)
ROOT_URLCONF = 'config.urls'

# Настройки шаблонов HTML
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],  # Папка с HTML-шаблонами
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# База данных — SQLite (файл db.sqlite3 в корне проекта)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Наша кастомная модель пользователя
AUTH_USER_MODEL = 'users.User'

# Адреса для входа/выхода
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Статические файлы (CSS, JS, картинки)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Язык и часовой пояс
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
