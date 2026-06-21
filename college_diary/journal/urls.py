from django.urls import path
from . import views

urlpatterns = [
    path('',                       views.home,          name='home'),
    path('schedule/',              views.schedule,      name='schedule'),
    path('journal/',               views.journal,       name='journal'),
    path('journal/add/',           views.lesson_add,    name='lesson_add'),
    path('journal/<int:pk>/',      views.lesson_detail, name='lesson_detail'),
    path('grades/',                views.my_grades,     name='my_grades'),
    path('attendance/',            views.my_attendance, name='my_attendance'),
    path('group/<int:pk>/stats/',  views.group_stats,   name='group_stats'),
]
