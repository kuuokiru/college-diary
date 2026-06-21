# ======================================================
# МАРШРУТЫ (URLs) — главный файл
# Здесь указывается какой адрес → какое приложение
# ======================================================

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),                          # Панель администратора
    path('login/',  auth_views.LoginView.as_view(             # Страница входа
        template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Выход
    path('', include('journal.urls')),                        # Основные страницы журнала
    path('users/', include('users.urls')),                    # Страницы пользователей
]
