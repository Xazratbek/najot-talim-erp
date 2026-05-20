from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from exams.models import Exam
from gamification.models import Rating, XP, XPReasonChoices
from groups.models import Group, GroupLesson, GroupStudent
from homeworks.models import *
from lessons.models import Lesson, LessonRating
from notifications.models import NotificationPreference
from payments.models import Payment
from shop.models import Category, Order, Product
from users.models import Roles, User
from lessons.models import LessonRating, Lesson
from django.http import JsonResponse

LEVEL_XP_STEP = 375

class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == Roles.STUDENT
        )

    def stats(self):
        student = self.request.user
        xp_agg = XP.objects.filter(student=student).aggregate(
            total_xp=Sum("amount"),
            total_kumush=Sum("kumushlar"),
        )
        total_xp = xp_agg["total_xp"] or 0
        total_kumush = xp_agg["total_kumush"] or student.balance
        rating = Rating.objects.filter(student=student).first()
        level = rating.level if rating else 1
        higher = (
            User.objects.filter(role=Roles.STUDENT)
            .annotate(xp_sum=Sum("xps__amount"))
            .filter(xp_sum__gt=total_xp)
            .count()
        )
        return {
            "total_xp": total_xp,
            "total_kumush": total_kumush,
            "level": level,
            "next_level_xp": level * LEVEL_XP_STEP,
            "overall_rank": higher + 1,
            "rating": rating,
        }

    def sidebar(self):
        s = self.stats()
        return {"sidebar_kumush": s["total_kumush"], "sidebar_level": s["level"]}


class StudentDashboardView(StudentRequiredMixin, View):
    template_name = "students/dashboard.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                **self.stats(),
                **self.sidebar()
            },
        )


class StudentPaymentsView(StudentRequiredMixin, View):
    template_name = "students/payments.html"

    def get(self, request):
        student = request.user
        status = request.GET.get("status", "").strip()
        from_date = request.GET.get("from_date", "").strip()
        to_date = request.GET.get("to_date", "").strip()
        page_num = request.GET.get("page", "1")

        payments = Payment.objects.filter(student=student).order_by("-paid_at")
        if status:
            payments = payments.filter(status=status)
        if from_date:
            payments = payments.filter(paid_at__date__gte=from_date)
        if to_date:
            payments = payments.filter(paid_at__date__lte=to_date)

        page_obj = Paginator(payments, 15).get_page(page_num)

        return render(
            request,
            self.template_name,
            {
                **self.sidebar(),
                "payments": page_obj,
                "page_obj": page_obj,
                "filters": {
                    "status": status,
                    "from_date": from_date,
                    "to_date": to_date,
                },
            },
        )


class StudentGroupsView(StudentRequiredMixin, View):
    template_name = "students/groups.html"

    def get(self, request):
        student = request.user
        tab = request.GET.get("tab", "active")
        today = date.today()
        groups = Group.objects.filter(students__student=student).distinct()

        if tab == "finished":
            groups = groups.filter(ended_at__lt=today)
        else:
            groups = groups.filter(
                Q(ended_at__isnull=True) | Q(ended_at__gte=today)
            )

        groups = groups.select_related("course", "course__category").prefetch_related(
            "teachers__teacher"
        )

        return render(
            request,
            self.template_name,
            {"groups": groups, "tab": tab, **self.sidebar()},
        )


class StudentGroupDetailView(StudentRequiredMixin, View):
    template_name = "students/group_detail.html"

    def get(self, request, pk):
        student = request.user
        status_filter = request.GET.get("status", "").strip()

        group = get_object_or_404(
            Group.objects.filter(students__student=student)
            .select_related("course"),
            pk=pk,
        )

        rows = []
        for gl in GroupLesson.objects.filter(group=group).select_related("lesson"):
            homework = Homework.objects.filter(group_lesson=gl).first()
            if not homework:
                status_key, status_label, video_count = "not_assigned", "Berilmagan", 0
                deadline = None
            else:
                video_count = homework.homework_files.count()
                sub = HomeworkSubmission.objects.filter(
                    homework=homework, student=student
                ).first()
                if not sub:
                    status_key, status_label = "not_submitted", "Bajarilmagan"
                else:
                    status_key = sub.status
                    status_label = sub.get_status_display()
                deadline = homework.deadline

            if status_filter and status_key != status_filter:
                continue

            rows.append(
                {
                    "type": "lesson",
                    "title": gl.lesson.title,
                    "video_count": video_count,
                    "status_key": status_key,
                    "status_label": status_label,
                    "deadline": deadline,
                    "lesson_date": gl.lesson.lesson_date,
                    "pk": gl.pk,
                }
            )

        if not status_filter or status_filter == "not_assigned":
            for exam in Exam.objects.filter(group=group):
                rows.append(
                    {
                        "type": "exam",
                        "title": exam.title,
                        "video_count": None,
                        "status_key": "not_assigned",
                        "status_label": "Berilmagan",
                        "deadline": exam.ended_at,
                        "lesson_date": exam.started_at.date(),
                        "pk": exam.pk,
                    }
                )

        rows.sort(key=lambda r: r["lesson_date"], reverse=True)

        return render(
            request,
            self.template_name,
            {
                "group": group,
                "rows": rows,
                "status_filter": status_filter,
                **self.sidebar(),
            },
        )


class StudentLessonDetailView(StudentRequiredMixin, View):
    template_name = "students/lesson_detail.html"

    def get(self, request, pk):
        student = request.user
        group_lesson = get_object_or_404(
            GroupLesson.objects.filter(group__students__student=student)
            .select_related("lesson", "group", "group__course"),
            pk=pk,
        )

        homework = Homework.objects.filter(group_lesson=group_lesson).first()
        submission = None
        homework_files = []
        submission_files = []
        can_submit = False
        description = ""

        if homework:
            homework_files = list(homework.homework_files.all())
            submission = (
                HomeworkSubmission.objects.filter(homework=homework, student=student)
                .select_related("checked_by")
                .first()
            )
            if homework.deadline >= timezone.now():
                can_submit = True

            if submission:
                submission_files = list(submission.homeworksubmission_files.all())
                description = submission.description
                can_submit = False

            elif (
                submission
                and submission.status == HomeWorkStatusChoices.REJECTED
                and submission.allow_resubmission
            ):
                can_submit = True

        already_rated = LessonRating.objects.filter(
            lesson=group_lesson.lesson, rated_by=student
        ).exists()

        return render(
            request,
            self.template_name,
            {
                "group_lesson": group_lesson,
                "homework": homework,
                "homework_files": homework_files,
                "submission": submission,
                "submission_files": submission_files,
                "description": description,
                "can_submit": can_submit,
                "already_rated": already_rated,
                "side_lessons": GroupLesson.objects.filter(group=group_lesson.group)
                .select_related("lesson")
                .order_by("-lesson__lesson_date"),
                **self.sidebar(),
            },
        )

    def post(self, request, pk):
        student = request.user
        group_lesson = get_object_or_404(
            GroupLesson.objects.filter(group__students__student=student),
            pk=pk,
        )
        homework = get_object_or_404(Homework, group_lesson=group_lesson)
        submission = HomeworkSubmission.objects.filter(
            homework=homework, student=student
        ).first()

        if homework.deadline < timezone.now():
            if not (
                submission
                and submission.status == HomeWorkStatusChoices.REJECTED
                and submission.allow_resubmission
            ):
                messages.error(request, "Uyga vazifa muddati tugagan.")
                return redirect("student-lesson-detail", pk=pk)

        description = request.POST.get("description", "").strip()
        submission = submission or HomeworkSubmission(
            homework=homework, student=student
        )
        submission.description = description
        submission.status = HomeWorkStatusChoices.WAITING
        submission.save()

        for f in request.FILES.getlist("files"):
            HomeworkSubmissionFiles.objects.create(
                homework_submission=submission, file=f
            )

        messages.success(request, "Uyga vazifa yuborildi.")
        return redirect("student-lesson-detail", pk=pk)


class StudentRateLessonView(StudentRequiredMixin, View):
    def post(self, request):
        student = request.user
        lesson_id = request.POST.get("lesson_id")
        star = request.POST.get("star")
        description = (request.POST.get("description") or "").strip()

        lesson = Lesson.objects.filter(id=lesson_id).first()
        if lesson_id and lesson:
            rate_exists = LessonRating.objects.filter(lesson=lesson, rated_by=student).exists()
            if rate_exists:
                messages.info(request, "Siz oldin bu darsga baxo bergansiz")
                return JsonResponse({"message": "Siz oldin bu darsga baxo bergansiz", "status": 400})

            LessonRating.objects.create(
                lesson=lesson,
                rated_by=student,
                star=star,
                description=description,
            )
            return JsonResponse({"message": f"{lesson.title}-darsi baholandi", "status": 201})

        return JsonResponse({"message": "Dars topilmadi", "status": 404})


class StudentIndicatorsView(StudentRequiredMixin, View):
    template_name = "students/indicators.html"

    def get(self, request):
        student = request.user
        by_reason = {}
        for reason, label in XPReasonChoices.choices:
            agg = XP.objects.filter(student=student, reason=reason).aggregate(
                xp=Sum("amount"), kumush=Sum("kumushlar")
            )
            by_reason[reason] = {
                "label": label,
                "xp": agg["xp"] or 0,
                "kumush": agg["kumush"] or 0,
            }

        return render(
            request,
            self.template_name,
            {**self.stats(), "by_reason": by_reason, **self.sidebar()},
        )


class StudentIndicatorsDetailView(StudentRequiredMixin, View):
    template_name = "students/indicators_detail.html"

    def get(self, request, reason):
        student = request.user
        valid = dict(XPReasonChoices.choices)
        if reason not in valid:
            reason = XPReasonChoices.FOR_LESSON

        return render(
            request,
            self.template_name,
            {
                "entries": XP.objects.filter(student=student, reason=reason).order_by(
                    "-created_at"
                ),
                "reason": reason,
                "reason_label": valid[reason],
                **self.sidebar(),
            },
        )


class StudentRankingView(StudentRequiredMixin, View):
    template_name = "students/ranking.html"

    def get(self, request):
        student = request.user
        scope = request.GET.get("scope", "all")
        period = request.GET.get("period", "month")

        period_start = None
        if period == "week":
            period_start = timezone.now() - timedelta(days=7)
        elif period == "month":
            period_start = timezone.now() - timedelta(days=30)
        elif period == "3month":
            period_start = timezone.now() - timedelta(days=90)

        xp_filter = Q()
        if period_start:
            xp_filter = Q(xps__created_at__gte=period_start)

        qs = User.objects.filter(role=Roles.STUDENT).annotate(
            total_xp=Sum("xps__amount", filter=xp_filter)
        )

        if scope == "branch" and student.branch_id:
            qs = qs.filter(branch_id=student.branch_id)

        elif scope == "group":
            group_ids = GroupStudent.objects.filter(student=student).values_list(
                "group_id", flat=True
            )
            member_ids = GroupStudent.objects.filter(
                group_id__in=group_ids
            ).values_list("student_id", flat=True)
            qs = qs.filter(id__in=member_ids)

        ordered = qs.order_by("-total_xp", "id")
        my_rank = None
        for i, u in enumerate(ordered, start=1):
            if u.id == student.id:
                my_rank = i
                break

        return render(
            request,
            self.template_name,
            {
                "rankings": ordered[:50],
                "my_rank": my_rank,
                "scope": scope,
                "period": period,
                **self.sidebar(),
            },
        )


class StudentShopView(StudentRequiredMixin, View):
    template_name = "students/shop.html"

    def get(self, request):
        student = request.user
        tab = request.GET.get("tab", "sale")
        category = request.GET.get("category", "").strip()
        price_from = request.GET.get("price_from", "").strip()
        price_to = request.GET.get("price_to", "").strip()
        search = request.GET.get("search", "").strip()
        affordable = request.GET.get("affordable_only") == "1"

        products = Product.objects.select_related("category").filter(stock__gt=0)
        if category:
            products = products.filter(category_id=category)
        if price_from.isdigit():
            products = products.filter(price__gte=int(price_from))
        if price_to.isdigit():
            products = products.filter(price__lte=int(price_to))
        if search:
            products = products.filter(title__icontains=search)
        if affordable:
            products = products.filter(price__lte=student.balance)

        return render(
            request,
            self.template_name,
            {
                "tab": tab,
                "products": products,
                "purchases": Order.objects.filter(student=student).select_related(
                    "product"
                ),
                "categories": Category.objects.all(),
                "filters": {
                    "category": category,
                    "price_from": price_from,
                    "price_to": price_to,
                    "search": search,
                    "affordable_only": affordable,
                },
                **self.sidebar(),
            },
        )

    def post(self, request):
        student = request.user
        product = get_object_or_404(Product, pk=request.POST.get("product_id"))
        if student.balance < product.price:
            messages.error(request, "Kumushingiz yetarli emas.")
        elif product.stock < 1:
            messages.error(request, "Mahsulot tugagan.")
        else:
            student.balance -= product.price
            student.save(update_fields=["balance"])
            product.stock -= 1
            product.save(update_fields=["stock"])
            Order.objects.create(student=student, product=product)
            messages.success(request, f"{product.title} sotib olindi.")
        return redirect(reverse("student-shop") + "?tab=sale")


class StudentSettingsView(StudentRequiredMixin, View):
    template_name = "students/settings.html"

    def get(self, request):
        student = request.user
        prefs, _ = NotificationPreference.objects.get_or_create(user=student)
        return render(
            request,
            self.template_name,
            {"student": student, "prefs": prefs, **self.sidebar()},
        )

    def post(self, request):
        student = request.user
        action = request.POST.get("action")

        if action == "profile":
            student.first_name = request.POST.get("first_name", student.first_name)
            student.last_name = request.POST.get("last_name", student.last_name)
            student.phone = request.POST.get("phone", student.phone)
            student.gender = request.POST.get("gender", student.gender) or None
            if request.FILES.get("avatar"):
                student.avatar = request.FILES["avatar"]
            student.save()
            messages.success(request, "Profil yangilandi.")

        elif action == "notifications":
            prefs, _ = NotificationPreference.objects.get_or_create(user=student)
            for field in (
                "new_exam",
                "new_lesson",
                "exam_announcement",
                "xp_update",
                "exam_deadline_near",
                "homework_reviewed",
                "added_to_group",
                "removed_from_group",
                "silver_rewarded",
            ):
                setattr(prefs, field, field in request.POST)
            prefs.save()
            messages.success(request, "Bildirishnoma sozlamalari saqlandi.")

        elif action == "password":
            return redirect("student-password-change")

        return redirect("student-settings")


class StudentPasswordChangeView(StudentRequiredMixin, PasswordChangeView):
    template_name = "students/password_change.html"
    success_url = reverse_lazy("student-settings")
