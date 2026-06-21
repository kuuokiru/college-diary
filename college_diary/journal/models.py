# ======================================================
# МОДЕЛИ ЖУРНАЛА
# Subject    — предметы/дисциплины
# ClassRoom  — учебные группы
# Lesson     — занятия (пары)
# Grade      — оценки студентов
# Attendance — посещаемость
# ======================================================

from django.db import models
from django.conf import settings


class Subject(models.Model):
    """Учебный предмет / дисциплина"""
    name = models.CharField(max_length=200, verbose_name='Название')

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    """Учебная группа"""
    name     = models.CharField(max_length=30, verbose_name='Группа')
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True,
        related_name='classrooms', verbose_name='Студенты',
        limit_choices_to={'role': 'student'}
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Занятие (пара)"""
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, verbose_name='Группа')
    subject   = models.ForeignKey(Subject,   on_delete=models.CASCADE, verbose_name='Предмет')
    teacher   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='lessons', verbose_name='Преподаватель',
        limit_choices_to={'role': 'teacher'}
    )
    date          = models.DateField(verbose_name='Дата')
    period_number = models.PositiveSmallIntegerField(default=1, verbose_name='Номер пары')
    topic         = models.CharField(max_length=255, blank=True, verbose_name='Тема занятия')
    homework      = models.TextField(blank=True, verbose_name='Домашнее задание')

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['date', 'period_number']

    def __str__(self):
        return f'{self.date} | {self.subject} | {self.classroom}'


class Grade(models.Model):
    """Оценка студента за конкретное занятие"""
    GRADE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    lesson  = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades', verbose_name='Занятие')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='grades', verbose_name='Студент',
        limit_choices_to={'role': 'student'}
    )
    value      = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, verbose_name='Оценка')
    comment    = models.CharField(max_length=255, blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('lesson', 'student')

    def __str__(self):
        return f'{self.student} — {self.value}'


class Attendance(models.Model):
    """Посещаемость студента на занятии"""
    STATUS_PRESENT = 'P'
    STATUS_ABSENT  = 'A'
    STATUS_LATE    = 'L'
    STATUS_CHOICES = [
        (STATUS_PRESENT, '✅ Присутствует'),
        (STATUS_ABSENT,  '❌ Отсутствует'),
        (STATUS_LATE,    '⏰ Опоздал'),
    ]

    lesson  = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendance', verbose_name='Занятие')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='attendance', verbose_name='Студент',
        limit_choices_to={'role': 'student'}
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PRESENT, verbose_name='Статус')
    note   = models.CharField(max_length=255, blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        unique_together = ('lesson', 'student')

    def __str__(self):
        return f'{self.student} — {self.get_status_display()}'
