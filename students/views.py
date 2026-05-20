from django.shortcuts import render
from users.models import User, Roles
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from gamification.models import XP, Rating
from django.db.models import Sum
from payments.models import Payment
from django.db.models import Q

class StudentDashboardView(UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == Roles.STUDENT

    def get(self, request):
        student = request.user
        total_amount_xp = XP.objects.filter(student=student).aggregate(total_amount=Sum('amount'))
        rating = Rating.objects.filter(student=student).first()

        return render(request,'students/dashboard.html',context={"total_amount_xp":total_amount_xp,'rating':rating})

class StudentPaymentsView(UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == Roles.STUDENT

    def get(self, request):
        student = request.user
        query = Payment.objects.filter(student=student)
        payment_status = request.POST.get('payment_status')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if payment_status:
            query = query.filter(status=payment_status)
        if from_date:
            query = query.filter(paid_at__gte=from_date)
        if to_date:
            query = query.filter(paid_at__lte=to_date)

        return render(request,'students/payments.html',context={'payments':query})