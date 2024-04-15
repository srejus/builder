from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *

# Create your views here.

class LoginView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'login.html',{'err':err})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            acc = Account.objects.get(user=user)
            if acc.role == 'CUSTOMER':
                return redirect("/")
            if acc.role == 'ARCHITECT':
                return redirect("/architect/dashboard")
            
        err = "Invalid credentails!"
        return redirect(f"/accounts/login/?err={err}")
    

class SignupView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'signup.html',{'err':err})
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        domain = request.POST.get('domain')
        role = request.POST.get('role')
        company_name = request.POST.get('company_name')

        if password != password2:
            err = "Password not matching!"
            return redirect(f"/accounts/signup?err={err}")
    
        user = User.objects.filter(username=username)
        if user.exists():
            err = "User with this username already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        acc = Account.objects.filter(email=email).exists()
        if acc:
            err = "User with this phone or email already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        user = User.objects.create_user(username=username,email=email,password=password)
        acc = Account.objects.create(user=user,first_name=first_name,last_name=last_name,
                                     email=email,location=location,
                                     domain=domain,company_name=company_name,role=role)

        type_ = request.GET.get("type")
        if type_ and type_ == 'admin':
            return redirect("/adminuser/users")
        
        return redirect('/accounts/login')


    

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/accounts/login/")
    

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request,id=None):
        if id:
            acc = Account.objects.get(id=id)
        else:
            acc = Account.objects.get(user=request.user)        
        return render(request,'profile.html',{'acc':acc})
    
    def post(self,request,id=None):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        domain = request.POST.get('domain')
        company_name = request.POST.get('company_name')

        if id:
            acc = Account.objects.get(id=id)
        else:
            acc = Account.objects.get(user=request.user)

        acc.first_name = first_name
        acc.last_name = last_name
        acc.email = email
        acc.location = location
        acc.domain = domain
        acc.company_name = company_name
        acc.save()

        if id:
            return redirect("/adminuser/users")

        return redirect("/")