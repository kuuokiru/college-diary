import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from users.models import User
from journal.models import Subject, ClassRoom, Lesson, Grade
from datetime import date, timedelta
import random

random.seed(42)

print("Очищаем старые данные...")
Grade.objects.all().delete()
Lesson.objects.all().delete()
ClassRoom.objects.all().delete()
Subject.objects.all().delete()
User.objects.all().delete()

print("Создаём пользователей...")

# Суперпользователь
admin = User.objects.create_superuser(
    'admin', 'admin@imsit.ru', 'pass123',
    first_name='Чернякин', last_name='С.М.', role='admin'
)

# Преподаватели
teachers_data = [
    ('gricyk',      'Грицык',      'Е.А.',  'gricyk@imsit.ru'),
    ('glushkov',    'Глушков',     'А.А.',  'glushkov@imsit.ru'),
    ('kochura',     'Кочура',      'А.Н.',  'kochura@imsit.ru'),
    ('rassokha',    'Рассоха',     'Е.В.',  'rassokha@imsit.ru'),
    ('shauluhova',  'Шаулухова',   'Н.В.',  'shauluhova@imsit.ru'),
    ('kochetkov',   'Кочетков',    'Р.В.',  'kochetkov@imsit.ru'),
    ('selyutina',   'Селютина',    'О.В.',  'selyutina@imsit.ru'),
    ('fizruk',      'Кафедра',     'ФК',    'fk@imsit.ru'),
    ('inostranec',  'Иностранный', 'яз.',   'foreign@imsit.ru'),
]
teachers = {}
for uname, last, first, email in teachers_data:
    u = User.objects.create_user(uname, email, 'pass123',
        first_name=first, last_name=last, role='teacher')
    teachers[uname] = u

# Предметы
subjects_data = [
    ('Инструментальные средства разработки ПО',             'gricyk'),
    ('Иностранный язык в профессиональной деятельности',    'inostranec'),
    ('Математическое моделирование',                        'glushkov'),
    ('Поддержка и тестирование программных модулей',        'kochura'),
    ('Разработка мобильных приложений',                     'rassokha'),
    ('Разработка программных модулей',                      'kochura'),
    ('Стандартизация, сертификация и техническое документоведение', 'shauluhova'),
    ('Технология разработки программного обеспечения',      'kochetkov'),
    ('Физическая культура',                                 'fizruk'),
    ('Численные методы',                                    'selyutina'),
]
subjects = {}
for name, teacher_key in subjects_data:
    s = Subject.objects.create(name=name)
    subjects[name] = (s, teachers[teacher_key])

# Имена для студентов
last_names = [
    'Иванов','Смирнова','Кузнецов','Попова','Волков',
    'Новикова','Морозов','Петрова','Соколов','Козлова',
    'Лебедев','Никитина','Семёнов','Захарова','Егоров',
    'Орлова','Павлов','Степанова','Тихонов','Белова',
    'Фёдоров','Михайлова','Макаров','Соловьёва','Андреев',
    'Алексеева','Якушев','Романова','Борисов','Матвеева',
]
first_names = ['А.И.','Д.С.','М.В.','Е.А.','С.Д.','К.О.','Н.П.','А.Е.','В.М.','Т.С.']

print("Создаём группы и студентов...")

groups = []
student_counter = 1
for i in range(1, 11):
    group_name = f'23-СПО-ИСиП-{i:02d}'
    classroom = ClassRoom.objects.create(name=group_name)

    group_students = []
    for j in range(3):
        idx = (student_counter - 1) % len(last_names)
        fidx = (student_counter - 1) % len(first_names)
        uname = f'student{student_counter}'
        u = User.objects.create_user(uname, f'{uname}@imsit.ru', 'pass123',
            first_name=first_names[fidx],
            last_name=last_names[idx],
            role='student')
        group_students.append(u)
        student_counter += 1

    # В группу 23-СПО-ИСиП-08 добавляем Чернякина С.М. (admin)
    if i == 8:
        classroom.students.set(group_students + [admin])
    else:
        classroom.students.set(group_students)

    groups.append(classroom)

print("Создаём занятия и оценки...")

today = date.today()
subj_list = list(subjects.values())

# Для каждой группы создаём несколько занятий
for classroom in groups:
    for day_offset in [5, 3, 1]:
        lesson_date = today - timedelta(days=day_offset)
        subj, teacher = random.choice(subj_list)
        lesson = Lesson.objects.create(
            classroom=classroom,
            subject=subj,
            teacher=teacher,
            date=lesson_date,
            period_number=random.randint(1, 6),
            topic=f'Тема занятия по предмету {subj.name[:30]}',
            homework='Повторить пройденный материал'
        )
        # Оценки для студентов
        for student in classroom.students.filter(role='student'):
            Grade.objects.create(
                lesson=lesson,
                student=student,
                value=random.choices([3,4,5], weights=[2,4,4])[0]
            )

print()
print("=" * 55)
print("✅ Данные созданы!")
print("=" * 55)
print()
print("Аккаунты (пароль для всех: pass123)")
print("  admin      — Чернякин С.М. (администратор, группа 23-СПО-ИСиП-08)")
print("  gricyk     — Грицык Е.А. (преподаватель)")
print("  glushkov   — Глушков А.А. (преподаватель)")
print("  kochura    — Кочура А.Н. (преподаватель)")
print("  rassokha   — Рассоха Е.В. (преподаватель)")
print("  kochetkov  — Кочетков Р.В. (преподаватель)")
print("  student1   — студент группы 23-СПО-ИСиП-01")
print("  student22  — студент группы 23-СПО-ИСиП-08")
print()

# Добавляем посещаемость к существующим занятиям
print("Добавляем данные посещаемости...")
from journal.models import Attendance

for classroom in ClassRoom.objects.all():
    for lesson in classroom.lessons.all():
        for student in classroom.students.filter(role='student'):
            status = random.choices(['P','P','P','L','A'], weights=[6,6,6,2,1])[0]
            Attendance.objects.get_or_create(
                lesson=lesson, student=student,
                defaults={'status': status}
            )
print("Посещаемость добавлена!")
