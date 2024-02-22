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

