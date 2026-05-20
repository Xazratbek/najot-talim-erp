from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import LoginForm
from django.views import View
from django.contrib.auth import login,authenticate

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,'registration/login.html',context={'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,request.POST.get('login'),request.POST.get('password'))
            if user:
                login(request,user)
                return reverse_lazy('student-dashboard')
        else:
            return render(request,'registration/login.html',context={'form':form})