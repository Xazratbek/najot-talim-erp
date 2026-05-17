import os
import random
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth.hashers import make_password
from django.db import connection
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


BATCH_SIZE = 3000
PASSWORD = make_password("Test12345!")

FIRST_NAMES = [
    "Aziz",
    "Jasur",
    "Sherzod",
    "Bekzod",
    "Muhammadali",
    "Diyor",
    "Abror",
    "Sardor",
    "Shahzod",
    "Farrux",
    "Kamron",
    "Islom",
    "Asadbek",
    "Zafar",
    "Anvar",
    "Laziz",
    "Oybek",
    "Javohir",
    "Rustam",
    "Shoxrux",
    "Madina",
    "Nilufar",
    "Zilola",
    "Shahnoza",
    "Sevinch",
    "Mohira",
    "Dildora",
    "Gulnoza",
    "Shirin",
    "Malika",
]

LAST_NAMES = [
    "Karimov",
    "Ismoilov",
    "Abdullayev",
    "Raximov",
    "Sattorov",
    "Yuldashev",
    "Qodirov",
    "Tojiboyev",
    "Nazarov",
    "Tursunov",
    "Alimuhamedov",
    "Sobirov",
    "Ergashev",
    "Musayev",
    "Asqarov",
    "Xolmatov",
]


def random_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def unique_username(used):
    while True:
        username = str(random.randint(10000, 99999))
        if username not in used:
            used.add(username)
            return username


def chunked_bulk_create(model, data, batch_size=BATCH_SIZE):
    if not data:
        return

    model.objects.bulk_create(data, batch_size=batch_size)
    data.clear()


def reset_connection():
    connection.close()


def generate_data():
    random.seed(42)

    print("Cleaning old data...")

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

    print("Creating branches...")

    branch_objects = [
        Branch(
            name=f"Najot Ta'lim - Filial {i + 1}",
            address=f"Toshkent sh., {i + 1}-daha",
            phone=f"+99890{random.randint(1000000, 9999999)}",
        )
        for i in range(10)
    ]

    Branch.objects.bulk_create(branch_objects)
    branches = list(Branch.objects.all())

    print("Creating course categories...")

    category_names = [
        "Dasturlash",
        "Dizayn",
        "Marketing",
        "Til",
        "Biznes",
    ]

    CourseCategory.objects.bulk_create(
        [CourseCategory(title=name) for name in category_names]
    )

    course_categories = list(CourseCategory.objects.all())

    print("Creating courses...")

    course_titles = [
        "Python Backend",
        "Java Backend",
        "Frontend React",
        "Flutter",
        "UI UX",
        "SMM",
        "Project Management",
        "English IELTS",
        "Data Analytics",
        "AI Fundamentals",
    ]

    Course.objects.bulk_create(
        [
            Course(
                category=random.choice(course_categories),
                title=title,
                price=Decimal(random.randint(900000, 3000000)),
            )
            for title in course_titles
        ]
    )

    courses = list(Course.objects.all())

    print("Creating lessons...")

    Lesson.objects.bulk_create(
        [Lesson(title=f"Lesson {i + 1}") for i in range(80)]
    )

    lessons = list(Lesson.objects.all())

    print("Creating users...")

    used_usernames = set()

    role_pool = (
        ([Roles.ADMIN] * 3)
        + ([Roles.TEACHER] * 18)
        + ([Roles.SUPPORT_TEACHER] * 8)
        + ([Roles.STUDENT] * 80)
    )

    random.shuffle(role_pool)

    users_to_create = []

    for role in role_pool:
        first, last = random_name()

        users_to_create.append(
            User(
                username=unique_username(used_usernames),
                first_name=first,
                last_name=last,
                phone=f"+998{random.randint(88, 99)}{random.randint(1000000, 9999999)}",
                role=role,
                balance=random.randint(0, 5000000),
                branch=random.choice(branches),
                password=PASSWORD,
                is_active=True,
            )
        )

    User.objects.bulk_create(users_to_create, batch_size=1000)

    users = list(User.objects.all())

    teachers = [u for u in users if u.role == Roles.TEACHER]
    support_teachers = [u for u in users if u.role == Roles.SUPPORT_TEACHER]
    students = [u for u in users if u.role == Roles.STUDENT]

    print("Creating groups...")

    groups_to_create = []

    for i in range(35):
        started_at = date.today() - timedelta(days=random.randint(20, 200))

        ended_at = (
            None
            if random.random() < 0.8
            else started_at + timedelta(days=random.randint(40, 120))
        )

        groups_to_create.append(
            Group(
                name=f"Group-{i + 1}",
                course=random.choice(courses),
                branch=random.choice(branches),
                started_at=started_at,
                ended_at=ended_at,
                is_opened=ended_at is None,
            )
        )

    Group.objects.bulk_create(groups_to_create)

    groups = list(Group.objects.all())

    print("Creating group teachers and students...")

    group_teachers = []
    group_students = []

    students_by_group = {}

    for group in groups:
        group_teachers.append(
            GroupTeacher(
                group=group,
                teacher=random.choice(teachers),
            )
        )

        if support_teachers and random.random() < 0.5:
            group_teachers.append(
                GroupTeacher(
                    group=group,
                    teacher=random.choice(support_teachers),
                )
            )

        group_size = random.randint(15, 28)

        shuffled_students = students.copy()
        random.shuffle(shuffled_students)

        selected_students = shuffled_students[:group_size]

        students_by_group[group.id] = selected_students

        for st in selected_students:
            group_students.append(
                GroupStudent(
                    group=group,
                    student=st,
                    joined_at=group.started_at
                    + timedelta(days=random.randint(0, 15)),
                )
            )

    GroupTeacher.objects.bulk_create(group_teachers, batch_size=1000)
    GroupStudent.objects.bulk_create(group_students, batch_size=3000)

    reset_connection()

    print("Creating group lessons...")

    group_lessons = []

    for group in groups:
        selected_lessons = random.sample(
            lessons,
            k=random.randint(8, 14),
        )

        for lesson in selected_lessons:
            group_lessons.append(
                GroupLesson(
                    group=group,
                    lesson=lesson,
                )
            )

    GroupLesson.objects.bulk_create(group_lessons, batch_size=3000)

    all_group_lessons = list(
        GroupLesson.objects.select_related(
            "group",
            "lesson",
        )
    )

    reset_connection()

    print("Creating attendance and homeworks...")

    attendance_batch = []
    homework_batch = []

    for gl in all_group_lessons:
        grp_students = students_by_group.get(gl.group_id, [])

        for st in grp_students:
            attendance_batch.append(
                Attendance(
                    group_lesson=gl,
                    student=st,
                    status=(
                        Status.PRESENT
                        if random.random() > 0.18
                        else Status.ABSENT
                    ),
                )
            )

            if len(attendance_batch) >= BATCH_SIZE:
                chunked_bulk_create(Attendance, attendance_batch)

        if random.random() < 0.7:
            homework_batch.append(
                Homework(
                    group_lesson=gl,
                    description="Uyga vazifa",
                    deadline=timezone.now()
                    + timedelta(days=random.randint(2, 10)),
                    file="fake/homework.txt",
                )
            )

            if len(homework_batch) >= 1000:
                chunked_bulk_create(Homework, homework_batch, 1000)

    chunked_bulk_create(Attendance, attendance_batch)
    chunked_bulk_create(Homework, homework_batch, 1000)

    reset_connection()

    print("Creating homework submissions...")

    hw_submission_batch = []

    homeworks = Homework.objects.select_related(
        "group_lesson__group"
    ).iterator(chunk_size=1000)

    for hw in homeworks:
        grp_students = students_by_group.get(hw.group_lesson.group_id, [])

        for st in grp_students:
            if random.random() < 0.75:
                hw_submission_batch.append(
                    HomeworkSubmission(
                        homework=hw,
                        student=st,
                        description="Topshiriq bajarildi",
                        file="fake/submission.txt",
                    )
                )

                if len(hw_submission_batch) >= BATCH_SIZE:
                    chunked_bulk_create(
                        HomeworkSubmission,
                        hw_submission_batch,
                    )

    chunked_bulk_create(HomeworkSubmission, hw_submission_batch)

    reset_connection()

    print("Creating payments and XP...")

    payments_batch = []
    xp_batch = []

    for st in students:
        for _ in range(random.randint(2, 5)):
            payments_batch.append(
                Payment(
                    student=st,
                    amount=Decimal(random.randint(250000, 1800000)),
                    payment_type=random.choice(
                        PaymentTypeChoices.values
                    ),
                    paid_at=timezone.now()
                    - timedelta(days=random.randint(1, 365)),
                )
            )

            if len(payments_batch) >= BATCH_SIZE:
                chunked_bulk_create(Payment, payments_batch)

        for _ in range(random.randint(5, 12)):
            xp_batch.append(
                XP(
                    student=st,
                    amount=random.randint(5, 100),
                    reason=random.choice(
                        XPReasonChoices.values
                    ),
                )
            )

            if len(xp_batch) >= BATCH_SIZE:
                chunked_bulk_create(XP, xp_batch)

    chunked_bulk_create(Payment, payments_batch)
    chunked_bulk_create(XP, xp_batch)

    reset_connection()

    print("Creating shop data...")

    Category.objects.bulk_create(
        [
            Category(name="Kitob"),
            Category(name="Texnika"),
            Category(name="Sticker"),
            Category(name="Kiyim"),
        ]
    )

    categories = list(Category.objects.all())

    Product.objects.bulk_create(
        [
            Product(
                category=random.choice(categories),
                title=f"Mahsulot {i + 1}",
                price=random.randint(30000, 400000),
                image="fake/product.jpg",
                stock=random.randint(5, 80),
            )
            for i in range(40)
        ]
    )

    products = list(Product.objects.all())

    orders_batch = []

    for st in students:
        for _ in range(random.randint(1, 3)):
            orders_batch.append(
                Order(
                    student=st,
                    product=random.choice(products),
                )
            )

            if len(orders_batch) >= BATCH_SIZE:
                chunked_bulk_create(Order, orders_batch)

    chunked_bulk_create(Order, orders_batch)

    reset_connection()

    print("Creating exams...")

    exams_batch = []

    for group in groups:
        for i in range(random.randint(2, 3)):
            started = timezone.now() - timedelta(
                days=random.randint(5, 90)
            )

            exams_batch.append(
                Exam(
                    group=group,
                    title=f"{group.name} Exam {i + 1}",
                    description="Oraliq imtihon",
                    started_at=started,
                    ended_at=started + timedelta(hours=2),
                    allow_resubmission=random.random() < 0.3,
                )
            )

    Exam.objects.bulk_create(exams_batch, batch_size=1000)

    exams = Exam.objects.select_related("group").iterator(
        chunk_size=1000
    )

    print("Creating exam submissions...")

    teacher_pool = teachers + support_teachers

    exam_submission_batch = []

    for exam in exams:
        grp_students = students_by_group.get(exam.group_id, [])

        for st in grp_students:
            if random.random() < 0.8:
                checked = random.random() < 0.7

                exam_submission_batch.append(
                    ExamSubmission(
                        exam=exam,
                        student=st,
                        file="fake/exam_submission.txt",
                        description="Exam solved",
                        checked_by=(
                            random.choice(teacher_pool)
                            if checked
                            else None
                        ),
                        checked_at=(
                            timezone.now()
                            - timedelta(
                                days=random.randint(1, 20)
                            )
                            if checked
                            else None
                        ),
                    )
                )

                if len(exam_submission_batch) >= BATCH_SIZE:
                    chunked_bulk_create(
                        ExamSubmission,
                        exam_submission_batch,
                    )

    chunked_bulk_create(
        ExamSubmission,
        exam_submission_batch,
    )

    reset_connection()

    print("\nDONE ✅\n")

    print(f"Users: {User.objects.count()}")
    print(f"Groups: {Group.objects.count()}")
    print(f"Group Students: {GroupStudent.objects.count()}")
    print(f"Group Lessons: {GroupLesson.objects.count()}")
    print(f"Attendance: {Attendance.objects.count()}")
    print(f"Homework: {Homework.objects.count()}")
    print(f"Homework Submissions: {HomeworkSubmission.objects.count()}")
    print(f"Payments: {Payment.objects.count()}")
    print(f"XP: {XP.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Exams: {Exam.objects.count()}")
    print(f"Exam Submissions: {ExamSubmission.objects.count()}")


if __name__ == "__main__":
    generate_data()