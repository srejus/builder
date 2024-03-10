from django.shortcuts import render,redirect
from django.views import *
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from accounts.models import Account


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ArcView(View):
    def get(self,request):
        arcs = Account.objects.filter(role='ARCHITECT')
        return render(request,'arcs.html',{'arcs':arcs})
    

@method_decorator(login_required, name='dispatch')
class BookArchAppointmentView(View):
    def get(self,request,id):
        err = request.GET.get("err")
        arcs = Account.objects.filter(role='ARCHITECT',id=id).last()
        return render(request,'book_arc_appointment.html',{'err':err,'arc':arcs})
    
    def post(self,request,id):
        appointment_at_str = request.POST.get("appointment_at")
        appointment_for_id = id

        # Convert the appointment_at string to a datetime object
        appointment_at = timezone.make_aware(datetime.strptime(appointment_at_str, '%Y-%m-%dT%H:%M'))

        # Get the current datetime in the current timezone
        current_datetime = timezone.now()

        if appointment_at > current_datetime:
            acc = Account.objects.get(user=request.user)
            appointment_for = Account.objects.get(id=appointment_for_id)
            if not BookArcAppointment.objects.filter(user=acc,appointment_for=appointment_for).exists():
                BookArcAppointment.objects.create(user=acc,appointment_for=appointment_for,booking_date=appointment_at)
        else:
            err = "Please select a future datetime!"
            return redirect(f"/architect/book-appointment?err={err}")

        msg = "Appointment Booked Successfully!"
        return redirect(f"/?msg={msg}")
    

@method_decorator(login_required, name='dispatch')
class ViewWorksView(View):
    def get(self,request,id):
        acc = Account.objects.get(id=id)
        works = Works.objects.filter(user=acc)
        return render(request,'view_works.html',{'works':works})
    

@method_decorator(login_required, name='dispatch')
class BuyPlanView(View):
    def get(self,request,id):
        acc = Account.objects.get(id=id)
        plans = Plans.objects.filter(user=acc)
        return render(request,'buy_plans.html',{'works':plans})
    

@method_decorator(login_required,name='dispatch')
class ArcDashView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.role != 'ARCHITECT':
            return redirect("/")
        
        return render(request,'arc_dash.html')
    

@method_decorator(login_required,name='dispatch')
class ArcAppointmentView(View):
    def get(self,request):
        appointments = BookArcAppointment.objects.filter(appointment_for__user=request.user)
        return render(request,'arc_appointments.html',{'appointments':appointments})
    

@method_decorator(login_required,name='dispatch')
class ArcPlansView(View):
    def get(self,request):
        plans = Plans.objects.filter(user__user=request.user)
        return render(request,'arc_plans.html',{'plans':plans})
    

@method_decorator(login_required,name='dispatch')
class ArcPlanDeleteView(View):
    def get(self,request,id=None):
        plan = Plans.objects.get(id=id).delete()
        return redirect("/architect/plans")
    

@method_decorator(login_required,name='dispatch')
class ArcAddPlanView(View):
    def get(self,request):
        return render(request,'add_plan.html')


    def post(self,request):
        title = request.POST.get("title")
        cover = request.FILES.get("cover")
        plan = request.FILES.get("plan")

        acc = Account.objects.get(user=request.user)

        Plans.objects.create(user=acc,title=title,cover=cover,plan=plan)
        return redirect("/architect/plans")