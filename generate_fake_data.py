import os
import random
from datetime import date, datetime, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from attendance.models import Attendance, Status
from branches.models import Branch
from courses.models import Course, CourseCategory
from exams.models import Exam, ExamSubmission
from gamification.models import XP, XPReasonChoices
from groups.models import Group, GroupLesson, GroupStudent, GroupTeacher
from homeworks.models import Homework, HomeworkSubmission
from lessons.models import Lesson
from payments.models import Payment, PaymentTypeChoices
from shop.models import Category, Order, Product
from users.models import Roles, User


FIRST_NAMES = [
    "Aziz", "Jasur", "Sherzod", "Bekzod", "Muhammadali", "Diyor", "Abror", "Sardor", "Shahzod", "Farrux",
    "Kamron", "Islom", "Asadbek", "Zafar", "Anvar", "Laziz", "Oybek", "Javohir", "Rustam", "Shoxrux",
    "Madina", "Nilufar", "Zilola", "Shahnoza", "Sevinch", "Mohira", "Dildora", "Gulnoza", "Shirin", "Malika",
    "Rayhona", "Dilnoza", "Zuhra", "Munisa", "Nozima", "Saida", "Nargiza", "Mavluda", "Gulbahor", "Feruza",
]
LAST_NAMES = [
    "Karimov", "Ismoilov", "Abdullayev", "Raximov", "Sattorov", "Yuldashev", "Qodirov", "Tojiboyev", "Nazarov",
    "Tursunov", "Alimuhamedov", "Sobirov", "Ergashev", "Musayev", "Asqarov", "Xolmatov", "Mamatqulov", "Nurmurodov",
]


def random_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def unique_username(used: set[str]) -> str:
    while True:
        username = f"{random.randint(10000, 99999)}"
        if username not in used:
            used.add(username)
            return username


def fake_file(name: str, text: str) -> ContentFile:
    return ContentFile(text.encode("utf-8"), name=name)


@transaction.atomic
def generate_data():
    random.seed(42)

    print("Eski fake ma'lumotlar tozalanmoqda...")
    models = [
        ExamSubmission,
        Exam,
        HomeworkSubmission,
        Homework,
        Attendance,
        GroupLesson,
        GroupTeacher,
        GroupStudent,
        Group,
        Payment,
        XP,
        Order,
        Product,
        Category,
        Lesson,
        Course,
        CourseCategory,
        User,
        Branch,
    ]
    for model in models:
        model.objects.all().delete()

    print("Branchlar yaratilmoqda...")
    branches = [
        Branch.objects.create(
            name=f"Najot Ta'lim - Filial {i + 1}",
            address=f"Toshkent sh., {i + 1}-daha, {random.randint(1, 120)}-uy",
            phone=f"+99890{random.randint(1000000, 9999999)}",
        )
        for i in range(30)
    ]

    print("Kurs kategoriyalari va kurslar yaratilmoqda...")
    category_names = ["Dasturlash", "Dizayn", "Marketing", "Til", "Biznes"]
    course_categories = [CourseCategory.objects.create(title=name) for name in category_names]

    course_titles = [
        "Python Backend", "Java Backend", "Frontend React", "Flutter Mobile", "UI/UX Design", "SMM Pro",
        "Project Management", "English IELTS", "Data Analytics", "AI Fundamentals", "DevOps Basics", "Cyber Security",
    ]
    courses = []
    for title in course_titles:
        courses.append(
            Course.objects.create(
                category=random.choice(course_categories),
                title=title,
                price=Decimal(random.randint(900000, 3200000)),
            )
        )

    print("Darslar yaratilmoqda...")
    lessons = [Lesson.objects.create(title=f"Lesson {i + 1}") for i in range(220)]

    print("Foydalanuvchilar yaratilmoqda...")
    used_usernames = set()
    users = []
    teachers = []
    students = []
    support_teachers = []

    role_pool = ([Roles.ADMIN] * 5) + ([Roles.TEACHER] * 30) + ([Roles.SUPPORT_TEACHER] * 15) + ([Roles.STUDENT] * 150)
    random.shuffle(role_pool)

    for i, role in enumerate(role_pool, start=1):
        first, last = random_name()
        user = User.objects.create(
            username=unique_username(used_usernames),
            first_name=first,
            last_name=last,
            phone=f"+998{random.randint(88, 99)}{random.randint(1000000, 9999999)}",
            role=role,
            balance=random.randint(0, 8_000_000),
            branch=random.choice(branches),
            password=make_password("Test12345!"),
            is_active=True,
        )
        users.append(user)
        if role == Roles.TEACHER:
            teachers.append(user)
        elif role == Roles.STUDENT:
            students.append(user)
        elif role == Roles.SUPPORT_TEACHER:
            support_teachers.append(user)

    print("Guruhlar va bog'lanishlar yaratilmoqda...")
    groups = []
    group_students_to_create = []
    group_teachers_to_create = []

    for i in range(90):
        started_at = date.today() - timedelta(days=random.randint(20, 280))
        ended_at = None if random.random() < 0.75 else started_at + timedelta(days=random.randint(60, 180))
        group = Group.objects.create(
            name=f"{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma'])}-{i + 1}",
            course=random.choice(courses),
            branch=random.choice(branches),
            started_at=started_at,
            ended_at=ended_at,
            is_opened=ended_at is None,
        )
        groups.append(group)

        group_teachers_to_create.append(GroupTeacher(group=group, teacher=random.choice(teachers)))
        if support_teachers and random.random() < 0.5:
            group_teachers_to_create.append(GroupTeacher(group=group, teacher=random.choice(support_teachers)))

        group_size = random.randint(25, 50)
        for student in random.sample(students, k=min(group_size, len(students))):
            group_students_to_create.append(
                GroupStudent(group=group, student=student, joined_at=started_at + timedelta(days=random.randint(0, 20)))
            )

    GroupTeacher.objects.bulk_create(group_teachers_to_create, batch_size=500)
    GroupStudent.objects.bulk_create(group_students_to_create, batch_size=2000)

    print("Group lessonlar, attendance va homeworks yaratilmoqda...")
    group_lessons = []
    for group in groups:
        selected_lessons = random.sample(lessons, k=random.randint(16, 28))
        for lesson in selected_lessons:
            group_lessons.append(GroupLesson(group=group, lesson=lesson))
    GroupLesson.objects.bulk_create(group_lessons, batch_size=2000)

    all_group_lessons = list(GroupLesson.objects.select_related("group", "lesson"))
    students_by_group = {}
    for gs in GroupStudent.objects.select_related("student", "group"):
        students_by_group.setdefault(gs.group_id, []).append(gs.student)

    attendance_to_create = []
    homework_to_create = []
    for gl in all_group_lessons:
        grp_students = students_by_group.get(gl.group_id, [])
        for st in grp_students:
            attendance_to_create.append(
                Attendance(
                    group_lesson=gl,
                    student=st,
                    status=Status.PRESENT if random.random() > 0.18 else Status.ABSENT,
                )
            )
        if random.random() < 0.72:
            homework_to_create.append(
                Homework(
                    group_lesson=gl,
                    description="Uyga vazifa: mavzu bo'yicha amaliy topshiriqlar.",
                    deadline=timezone.now() + timedelta(days=random.randint(2, 10)),
                    file=fake_file("homework.txt", "Homework description"),
                )
            )

    Attendance.objects.bulk_create(attendance_to_create, batch_size=5000)
    Homework.objects.bulk_create(homework_to_create, batch_size=500)

    print("Homework submissions yaratilmoqda...")
    hw_submissions = []
    for hw in Homework.objects.select_related("group_lesson__group"):
        grp_students = students_by_group.get(hw.group_lesson.group_id, [])
        for st in grp_students:
            if random.random() < 0.74:
                hw_submissions.append(
                    HomeworkSubmission(
                        homework=hw,
                        student=st,
                        description="Topshiriq bajarildi.",
                        file=fake_file("submission.txt", "Submission body"),
                    )
                )
    HomeworkSubmission.objects.bulk_create(hw_submissions, batch_size=1500)

    print("To'lovlar, XP va Shop ma'lumotlari yaratilmoqda...")
    payments = []
    xps = []
    for st in students:
        for _ in range(random.randint(2, 8)):
            payments.append(
                Payment(
                    student=st,
                    amount=Decimal(random.randint(250000, 2200000)),
                    payment_type=random.choice(PaymentTypeChoices.values),
                    paid_at=timezone.now() - timedelta(days=random.randint(1, 365)),
                )
            )
        for _ in range(random.randint(8, 20)):
            xps.append(
                XP(
                    student=st,
                    amount=random.randint(5, 120),
                    reason=random.choice(XPReasonChoices.values),
                )
            )
    Payment.objects.bulk_create(payments, batch_size=2000)
    XP.objects.bulk_create(xps, batch_size=3000)

    shop_categories = [Category.objects.create(name=n) for n in ["Kitob", "Aksesuar", "Texnika", "Kiyim", "Sticker"]]
    products = []
    for i in range(75):
        products.append(
            Product.objects.create(
                category=random.choice(shop_categories),
                title=f"Mahsulot {i + 1}",
                price=random.randint(30_000, 750_000),
                image=fake_file("product.jpg", "fakeimagecontent"),
                stock=random.randint(10, 200),
            )
        )

    orders = []
    for st in students:
        for _ in range(random.randint(1, 6)):
            orders.append(Order(student=st, product=random.choice(products)))
    Order.objects.bulk_create(orders, batch_size=2000)

    print("Imtihonlar va topshiriqlar yaratilmoqda...")
    exams = []
    for group in groups:
        for i in range(random.randint(2, 4)):
            started = timezone.now() - timedelta(days=random.randint(5, 120))
            ended = started + timedelta(hours=2)
            exams.append(
                Exam(
                    group=group,
                    title=f"{group.name} - Exam {i + 1}",
                    description="Oraliq nazorat imtihoni.",
                    started_at=started,
                    ended_at=ended,
                    allow_resubmission=random.random() < 0.35,
                )
            )
    Exam.objects.bulk_create(exams, batch_size=500)

    exam_submissions = []
    teacher_pool = teachers + support_teachers
    for exam in Exam.objects.select_related("group"):
        grp_students = students_by_group.get(exam.group_id, [])
        for st in grp_students:
            if random.random() < 0.81:
                exam_submissions.append(
                    ExamSubmission(
                        exam=exam,
                        student=st,
                        file=fake_file("exam_submission.txt", "Exam answer"),
                        description="Barcha savollarga javob berildi.",
                        checked_by=random.choice(teacher_pool) if random.random() < 0.7 else None,
                        checked_at=timezone.now() - timedelta(days=random.randint(1, 30)) if random.random() < 0.7 else None,
                    )
                )
    ExamSubmission.objects.bulk_create(exam_submissions, batch_size=2000)

    print("Tayyor ✅")
    print(f"Users: {User.objects.count()}")
    print(f"Branches: {Branch.objects.count()}")
    print(f"Groups: {Group.objects.count()}")
    print(f"Group students: {GroupStudent.objects.count()}")
    print(f"Group lessons: {GroupLesson.objects.count()}")
    print(f"Attendance: {Attendance.objects.count()}")
    print(f"Homeworks: {Homework.objects.count()}")
    print(f"Homework submissions: {HomeworkSubmission.objects.count()}")
    print(f"Payments: {Payment.objects.count()}")
    print(f"XP: {XP.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Exams: {Exam.objects.count()}")
    print(f"Exam submissions: {ExamSubmission.objects.count()}")


if __name__ == "__main__":
    generate_data()