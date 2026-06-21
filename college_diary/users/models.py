# ======================================================
# МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ
# Описывает таблицу пользователей в базе данных.
# Расширяет стандартного пользователя Django — добавляет поле "роль"
# ======================================================

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Константы ролей
    ROLE_ADMIN   = 'admin'
    ROLE_TEACHER = 'teacher'
    ROLE_STUDENT = 'student'
    ROLE_PARENT  = 'parent'

    # Список доступных ролей
    ROLES = [
        (ROLE_ADMIN,   'Администратор'),
        (ROLE_TEACHER, 'Преподаватель'),
        (ROLE_STUDENT, 'Студент'),
        (ROLE_PARENT,  'Родитель'),
    ]

    # Поле роли — добавляется к стандартным полям (имя, пароль, email и т.д.)
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=ROLE_STUDENT,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    # Удобные свойства для проверки роли в шаблонах
    @property
    def is_teacher(self):  return self.role == self.ROLE_TEACHER
    @property
    def is_student(self):  return self.role == self.ROLE_STUDENT
    @property
    def is_admin(self):    return self.role == self.ROLE_ADMIN
