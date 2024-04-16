from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *

# Create your views here.
class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated:
            acc = Account.objects.get(user=request.user)
            if acc.role == 'ARCHITECT':
                return redirect("/architect/dashboard")
            if acc.role == 'CONTRACTOR':
                return redirect("/contractor/") # change this to contractor home url
            
        msg = request.GET.get("msg")
        return render(request,'index.html',{'msg':msg})
    


@method_decorator(login_required, name='dispatch')
class RentItemsView(View):
    def get(self,request,id=None):
        items = RentItems.objects.all()
        return render(request,'rent_items.html',{'items':items})


@method_decorator(login_required, name='dispatch')
class PlaceOrderView(View):
    def get(self,request,id):
        item = RentItems.objects.get(id=id)
        err = request.GET.get("err")
        return render(request,'address.html',{'item':item,'err':err})
    
    def post(self,request,id):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        no_of_days = request.POST.get("no_of_days")
        qnty = request.POST.get("qnty")

        acc = Account.objects.get(user=request.user)
        item = RentItems.objects.get(id=id)

        if int(qnty) > item.available_quantity:
            err = "Out of Stock!"
            return redirect(f"/place-order/{id}?err={err}")
        RentOrder.objects.create(user=acc,item=item,quantity=qnty,no_of_days=no_of_days,name=name,phone=phone,address=address)

        msg = "Rent Order Placed Successfully!"
        return redirect(f"/?msg={msg}")


@method_decorator(login_required, name='dispatch')
class MyOrdersView(View):
    def get(self,request):
        orders = RentOrder.objects.filter(user__user=request.user)
        return render(request,'my_orders.html',{'orders':orders})