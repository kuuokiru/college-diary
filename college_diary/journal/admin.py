from django.contrib import admin
from .models import Subject, ClassRoom, Lesson, Grade, Attendance

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('students',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display  = ('date', 'period_number', 'subject', 'classroom', 'teacher', 'topic')
    list_filter   = ('date', 'subject', 'classroom', 'teacher')
    date_hierarchy = 'date'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'value', 'comment')
    list_filter  = ('value', 'lesson__subject')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'status', 'note')
    list_filter  = ('status',)
