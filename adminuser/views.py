from django.shortcuts import render,redirect
from django.views import View

from accounts.models import *
from home.models import RentOrder 

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(login_required,name='dispatch')
class AdminHomeView(View):
    def get(self,request):
        return render(request,'admin/home.html')
    

@method_decorator(login_required,name='dispatch')
class AdminUserView(View):
    def get(self,request):
        users = Account.objects.all().order_by('-id')
        return render(request,'admin/users.html',{'users':users})
    

@method_decorator(login_required,name='dispatch')
class AdminDeleteUserView(View):
    def get(self,request,id):
        user = Account.objects.get(id=id)
        user.delete()
        return redirect("/adminuser/users")


@method_decorator(login_required,name='dispatch')
class AdminEditUserView(View):
    def get(self,request,id):
        user = Account.objects.get(id=id)
        return render(request,'admin/edit_user.html',{'acc':user})


@method_decorator(login_required,name='dispatch')
class AdminAddUserView(View):
    def get(self,request):
        return render(request,'admin/add_user.html')


@method_decorator(login_required,name='dispatch')
class AdminRentedItemsView(View):
    def get(self,request):
        items = RentOrder.objects.all().order_by('-id')
        return render(request,'admin/rented_items.html',{'items':items})
    

@method_decorator(login_required,name='dispatch')
class AdminRentedItemsRestockView(View):
    def get(self,request,id=None):
        order = RentOrder.objects.get(id=id)
        item = order.item

        item.available_quantity += order.quantity
        item.save()

        order.is_restocked = True
        order.save()

        return redirect("/adminuser/rented-items")
