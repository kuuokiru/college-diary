# ======================================================
# ПРЕДСТАВЛЕНИЯ (VIEWS)
# ======================================================

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from django.http import JsonResponse
from .models import Lesson, Grade, ClassRoom, Subject, Attendance
from users.models import User


@login_required
def home(request):
    user = request.user
    context = {'user': user}

    if user.is_teacher:
        context['lessons'] = Lesson.objects.filter(teacher=user).order_by('-date')[:10]
        context['classes'] = ClassRoom.objects.filter(lesson__teacher=user).distinct()
        # Статистика по группам
        stats = []
        for cls in context['classes']:
            avg = Grade.objects.filter(lesson__classroom=cls, lesson__teacher=user).aggregate(a=Avg('value'))['a']
            stats.append({'name': cls.name, 'avg': round(avg, 1) if avg else '—'})
        context['class_stats'] = stats

    elif user.is_student:
        classrooms = user.classrooms.all()
        context['classrooms'] = classrooms
        context['grades']  = Grade.objects.filter(student=user).order_by('-lesson__date')[:20]
        avg = (Grade.objects.filter(student=user)
               .values('lesson__subject__name')
               .annotate(avg=Avg('value'))
               .order_by('lesson__subject__name'))
        context['avg_grades'] = avg

        # Данные для графика успеваемости (последние 8 недель)
        from datetime import date, timedelta
        weeks = []
        for w in range(7, -1, -1):
            week_start = date.today() - timedelta(days=date.today().weekday() + w*7)
            week_end   = week_start + timedelta(days=6)
            avg_w = Grade.objects.filter(
                student=user, lesson__date__range=(week_start, week_end)
            ).aggregate(a=Avg('value'))['a']
            weeks.append({'label': week_start.strftime('%d.%m'), 'avg': round(avg_w, 2) if avg_w else None})
        context['chart_labels'] = json.dumps([w['label'] for w in weeks])
        context['chart_data']   = json.dumps([w['avg'] for w in weeks])

        # Посещаемость студента
        att = Attendance.objects.filter(student=user)
        total   = att.count()
        present = att.filter(status='P').count()
        late    = att.filter(status='L').count()
        absent  = att.filter(status='A').count()
        context['att_total']   = total
        context['att_present'] = present
        context['att_late']    = late
        context['att_absent']  = absent
        context['att_pct']     = round((present + late) / total * 100) if total else 100

    elif user.is_admin or user.is_staff:
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
        context['total_lessons']  = Lesson.objects.count()
        context['classes']        = ClassRoom.objects.all()

    return render(request, 'journal/home.html', context)


@login_required
def schedule(request):
    user = request.user
    if user.is_teacher:
        lessons = Lesson.objects.filter(teacher=user).order_by('date', 'period_number')
    elif user.is_student:
        lessons = Lesson.objects.filter(classroom__in=user.classrooms.all()).order_by('date', 'period_number')
    else:
        lessons = Lesson.objects.all().order_by('date', 'period_number')

    grouped = {}
    for lesson in lessons:
        grouped.setdefault(lesson.date, []).append(lesson)

    return render(request, 'journal/schedule.html', {'grouped': grouped})


@login_required
def journal(request):
    user = request.user
    if user.is_student:
        return redirect('home')
    lessons = Lesson.objects.filter(teacher=user).order_by('-date') if user.is_teacher else Lesson.objects.all().order_by('-date')
    return render(request, 'journal/journal.html', {'lessons': lessons})


@login_required
def lesson_detail(request, pk):
    lesson   = get_object_or_404(Lesson, pk=pk)
    students = lesson.classroom.students.all().order_by('last_name', 'first_name')
    grades_map     = {g.student_id: g for g in Grade.objects.filter(lesson=lesson)}
    attendance_map = {a.student_id: a for a in Attendance.objects.filter(lesson=lesson)}

    if request.method == 'POST' and (request.user.is_teacher or request.user.is_staff):
        for student in students:
            # Оценки
            val     = request.POST.get(f'grade_{student.id}')
            comment = request.POST.get(f'comment_{student.id}', '')
            if val:
                Grade.objects.update_or_create(
                    lesson=lesson, student=student,
                    defaults={'value': int(val), 'comment': comment}
                )
            else:
                Grade.objects.filter(lesson=lesson, student=student).delete()

            # Посещаемость
            att_status = request.POST.get(f'att_{student.id}')
            att_note   = request.POST.get(f'att_note_{student.id}', '')
            if att_status:
                Attendance.objects.update_or_create(
                    lesson=lesson, student=student,
                    defaults={'status': att_status, 'note': att_note}
                )

        messages.success(request, 'Данные сохранены!')
        return redirect('lesson_detail', pk=pk)

    return render(request, 'journal/lesson_detail.html', {
        'lesson': lesson,
        'students': students,
        'grades_map': grades_map,
        'attendance_map': attendance_map,
    })


@login_required
def lesson_add(request):
    if not (request.user.is_teacher or request.user.is_staff):
        return redirect('home')

    if request.method == 'POST':
        classroom_id  = request.POST.get('classroom')
        subject_id    = request.POST.get('subject')
        date          = request.POST.get('date')
        period_number = request.POST.get('period_number', 1)
        topic         = request.POST.get('topic', '')
        homework      = request.POST.get('homework', '')
        teacher = request.user if request.user.is_teacher else get_object_or_404(User, pk=request.POST.get('teacher'))

        Lesson.objects.create(
            classroom_id=classroom_id, subject_id=subject_id,
            teacher=teacher, date=date, period_number=period_number,
            topic=topic, homework=homework,
        )
        messages.success(request, 'Занятие добавлено!')
        return redirect('journal')

    return render(request, 'journal/lesson_add.html', {
        'classrooms': ClassRoom.objects.all(),
        'subjects':   Subject.objects.all(),
        'teachers':   User.objects.filter(role='teacher'),
    })


@login_required
def my_grades(request):
    if not request.user.is_student:
        return redirect('home')
    grades = Grade.objects.filter(student=request.user).order_by('lesson__subject__name', 'lesson__date')
    grouped = {}
    for g in grades:
        grouped.setdefault(g.lesson.subject.name, []).append(g)
    return render(request, 'journal/my_grades.html', {'grouped': grouped})


@login_required
def my_attendance(request):
    """Посещаемость студента"""
    if not request.user.is_student:
        return redirect('home')
    att = Attendance.objects.filter(student=request.user).order_by('-lesson__date')
    grouped = {}
    for a in att:
        grouped.setdefault(a.lesson.subject.name, []).append(a)

    total   = att.count()
    present = att.filter(status='P').count()
    late    = att.filter(status='L').count()
    absent  = att.filter(status='A').count()
    pct     = round((present + late) / total * 100) if total else 100

    return render(request, 'journal/attendance.html', {
        'grouped': grouped,
        'total': total, 'present': present,
        'late': late, 'absent': absent, 'pct': pct,
    })


@login_required
def group_stats(request, pk):
    """Статистика по группе для преподавателя"""
    if not (request.user.is_teacher or request.user.is_staff):
        return redirect('home')
    classroom = get_object_or_404(ClassRoom, pk=pk)
    students  = classroom.students.all().order_by('last_name')

    student_stats = []
    for s in students:
        avg = Grade.objects.filter(student=s, lesson__classroom=classroom).aggregate(a=Avg('value'))['a']
        att = Attendance.objects.filter(student=s, lesson__classroom=classroom)
        total  = att.count()
        absent = att.filter(status='A').count()
        student_stats.append({
            'student': s,
            'avg': round(avg, 1) if avg else '—',
            'absent': absent,
            'total': total,
            'pct': round((total - absent) / total * 100) if total else 100,
        })

    return render(request, 'journal/group_stats.html', {
        'classroom': classroom,
        'student_stats': student_stats,
    })
