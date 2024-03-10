from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *

# Create your views here.
class IndexView(View):
    def get(self,request):
        msg = request.GET.get("msg")
        return render(request,'index.html',{'msg':msg})
    


@method_decorator(login_required, name='dispatch')
class RentItemsView(View):
    def get(self,request):
        items = RentItems.objects.all()
        return render(request,'rent_items.html',{'items':items})


@method_decorator(login_required, name='dispatch')
class PlaceOrderView(View):
    def get(self,request,id):
        qnty = request.GET.get("qnty")
        return render(request,'address.html')
    
    def post(self,request,id):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        no_of_days = request.POST.get("no_of_days")
        qnty = request.GET.get("qnty")

        acc = Account.objects.get(user=request.user)
        item = RentItems.objects.get(id=id)
        RentOrder.objects.create(user=acc,item=item,quantity=qnty,no_of_days=no_of_days,name=name,phone=phone,address=address)

        return redirect("/")


@method_decorator(login_required, name='dispatch')
class MyOrdersView(View):
    def get(self,request):
        orders = RentOrder.objects.filter(user__user=request.user)
        return render(request,'my_orders.html',{'orders':orders})