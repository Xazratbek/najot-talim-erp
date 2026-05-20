import os
import random
from datetime import date, datetime, time, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from attendance.models import Attendance, Status
from branches.models import Branch
from courses.models import Course, CourseCategory
from exams.models import Exam, ExamSubmission
from gamification.models import Rating, XP, XPReasonChoices
from groups.models import Group, GroupLesson, GroupStudent, GroupTeacher
from homeworks.models import Homework, HomeworkSubmission, HomeWorkStatusChoices
from lessons.models import Lesson, LessonRating
from notifications.models import Notification, NotificationPreference, NotificationTypes
from payments.models import Payment, PaymentStatusChoices, PaymentTypeChoices
from shop.models import Category, Order, Product
from users.models import GenderChoices, Roles, User


FIRST_NAMES = [
    "Aziz", "Jasur", "Sardor", "Muhammadali", "Bekzod", "Mirjalol", "Asilbek", "Ibrohim",
    "Ziyoda", "Malika", "Shahnoza", "Dilnoza", "Madina", "Gulnoza", "Sitora", "Sevara",
]
LAST_NAMES = [
    "Karimov", "Raximov", "Yusupov", "Tursunov", "Nazarov", "Qodirov", "Islomov", "Xudoyberdiyev",
    "To'rayeva", "Abdullayeva", "Usmonova", "Aliyeva", "Sobirova", "Yo'ldosheva", "Niyozova",
]
BRANCH_DATA = [
    ("Chilonzor", "Toshkent sh., Chilonzor tumani, Bunyodkor ko'chasi 12", "+998712001122"),
    ("Yunusobod", "Toshkent sh., Yunusobod tumani, Amir Temur ko'chasi 88", "+998712003344"),
    ("Samarqand", "Samarqand sh., Registon ko'chasi 5", "+998662220011"),
]
COURSE_DATA = {
    "Dasturlash": [
        ("Python Backend", Decimal("1200000"), 8),
        ("Frontend React", Decimal("1300000"), 7),
    ],
    "Til": [
        ("Ingliz tili IELTS", Decimal("950000"), 6),
        ("Rus tili", Decimal("700000"), 5),
    ],
}
LESSON_TOPICS = ["Variables va Data Types", "Functionlar", "Django ORM", "API yozish", "Test yozish"]


def random_phone():
    return "+9989{}{:07d}".format(random.choice([0, 1, 3, 4, 5, 7, 8, 9]), random.randint(0, 9999999))


def create_user(role, branch, idx):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    username = f"{idx:05d}"
    return User.objects.create_user(
        username=username,
        password="Test12345!",
        first_name=first,
        last_name=last,
        role=role,
        branch=branch,
        phone=random_phone(),
        gender=random.choice([GenderChoices.MALE, GenderChoices.FEMALE]),
        email=f"{first.lower()}.{last.lower()}{idx}@example.uz",
    )


def tiny_image(name="image.gif"):
    data = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )
    return ContentFile(data, name=name)


@transaction.atomic
def run():
    print("Oldingi test ma'lumotlar tozalanmoqda...")
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    Attendance.objects.all().delete()
    LessonRating.objects.all().delete()
    HomeworkSubmission.objects.all().delete()
    Homework.objects.all().delete()
    ExamSubmission.objects.all().delete()
    Exam.objects.all().delete()
    Payment.objects.all().delete()
    Notification.objects.all().delete()
    NotificationPreference.objects.all().delete()
    XP.objects.all().delete()
    Rating.objects.all().delete()
    GroupStudent.objects.all().delete()
    GroupTeacher.objects.all().delete()
    GroupLesson.objects.all().delete()
    Lesson.objects.all().delete()
    Group.objects.all().delete()
    Course.objects.all().delete()
    CourseCategory.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    Branch.objects.all().delete()

    branches = [Branch.objects.create(name=n, address=a, phone=p) for n, a, p in BRANCH_DATA]

    courses = []
    for category_title, items in COURSE_DATA.items():
        category = CourseCategory.objects.create(title=category_title)
        for title, price, duration in items:
            courses.append(Course.objects.create(category=category, title=title, price=price, duration_in_month=duration))

    teachers = [create_user(Roles.TEACHER, random.choice(branches), i) for i in range(100, 106)]
    students = [create_user(Roles.STUDENT, random.choice(branches), i) for i in range(1000, 1060)]

    now = timezone.now()
    groups = []
    for i in range(1, 7):
        course = random.choice(courses)
        branch = random.choice(branches)
        start = date.today() - timedelta(days=random.randint(20, 120))
        group = Group.objects.create(
            name=f"{course.title} #{i} ({branch.name})",
            course=course,
            branch=branch,
            started_at=start,
            ended_at=None,
            is_opened=True,
            max_students=28,
        )
        groups.append(group)
        GroupTeacher.objects.create(group=group, teacher=random.choice(teachers))

        group_students = random.sample(students, k=12)
        for st in group_students:
            GroupStudent.objects.create(group=group, student=st, joined_at=start + timedelta(days=random.randint(0, 7)))

        for topic in LESSON_TOPICS:
            lesson = Lesson.objects.create(title=f"{course.title}: {topic}")
            gl = GroupLesson.objects.create(group=group, lesson=lesson)

            for st in group_students:
                Attendance.objects.create(
                    group_lesson=gl,
                    student=st,
                    status=random.choices([Status.PRESENT, Status.ABSENT], weights=[88, 12], k=1)[0],
                )
                LessonRating.objects.create(
                    lesson=lesson,
                    rated_by=st,
                    star=random.randint(3, 5),
                    description=random.choice([
                        "Mavzu aniq tushuntirildi.",
                        "Amaliy misollar juda foydali bo'ldi.",
                        "Dars dinamik va tushunarli o'tdi.",
                    ]),
                )

            hw = Homework.objects.create(
                group_lesson=gl,
                description=f"{topic} bo'yicha amaliy topshiriq va kod review.",
                deadline=now + timedelta(days=random.randint(2, 10)),
            )
            for st in group_students:
                HomeworkSubmission.objects.create(
                    homework=hw,
                    student=st,
                    description=random.choice([
                        "Topshiriqni to'liq bajardim.",
                        "Bir nechta savollarim bor.",
                        "Qo'shimcha optimizatsiya qildim.",
                    ]),
                    status=random.choice([
                        HomeWorkStatusChoices.APPROVED,
                        HomeWorkStatusChoices.WAITING,
                        HomeWorkStatusChoices.NOT_SUBMITTED,
                    ]),
                )

        exam_start = datetime.combine(date.today() + timedelta(days=5), time(10, 0), tzinfo=timezone.get_current_timezone())
        exam = Exam.objects.create(
            group=group,
            title=f"{course.title} Oraliq nazorat",
            description="Nazariy savollar va amaliy masalalardan iborat imtihon.",
            started_at=exam_start,
            ended_at=exam_start + timedelta(hours=2),
            allow_resubmission=False,
        )
        for gs in group.students.select_related("student"):
            ExamSubmission.objects.create(
                exam=exam,
                student=gs.student,
                description="Savollarga ketma-ket javob berildi.",
                checked_by=random.choice(teachers),
                checked_at=now - timedelta(days=random.randint(0, 2)),
            )

    for st in students:
        Payment.objects.create(
            student=st,
            amount=random.choice([Decimal("700000"), Decimal("950000"), Decimal("1200000"), Decimal("1300000")]),
            payment_type=random.choice([PaymentTypeChoices.CLICK, PaymentTypeChoices.PAYME, PaymentTypeChoices.CARD]),
            paid_at=now - timedelta(days=random.randint(1, 45)),
            status=random.choice([PaymentStatusChoices.PAID, PaymentStatusChoices.PAID, PaymentStatusChoices.UNCONFIRMED]),
        )
        XP.objects.create(
            student=st,
            amount=random.randint(30, 300),
            kumushlar=random.randint(3, 30),
            reason=random.choice(XPReasonChoices.values),
        )
        Rating.objects.create(student=st, level=random.randint(1, 7))
        NotificationPreference.objects.create(user=st)
        Notification.objects.create(
            receiver=st,
            type=random.choice(NotificationTypes.values),
            title=random.choice([
                "Yangi dars jadvalga qo'shildi",
                "Uyga vazifa tekshirildi",
                "Imtihon vaqti yaqinlashmoqda",
            ]),
            is_read=random.choice([True, False]),
        )

    shop_categories = [Category.objects.create(name=name) for name in ["Kitoblar", "Aksessuarlar", "Elektronika"]]
    products = []
    for i in range(1, 7):
        p = Product.objects.create(
            category=random.choice(shop_categories),
            title=random.choice([
                "Python 3 qo'llanma",
                "Brend daftar to'plami",
                "Simsiz sichqoncha",
                "USB flash 64GB",
                "Ingliz tili test to'plami",
            ]) + f" {i}",
            price=random.randint(50000, 350000),
            image=tiny_image(f"product_{i}.gif"),
            stock=random.randint(5, 40),
        )
        products.append(p)

    for st in random.sample(students, k=25):
        Order.objects.create(student=st, product=random.choice(products))

    print("Tayyor ✅ Realistik test ma'lumotlar yaratildi.")
    print(f"Filiallar: {Branch.objects.count()}, O'quvchilar: {len(students)}, O'qituvchilar: {len(teachers)}, Guruhlar: {len(groups)}")


if __name__ == "__main__":
    run()
