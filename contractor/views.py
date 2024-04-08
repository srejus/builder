from django.shortcuts import render,redirect
from django.views import *
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from accounts.models import Account
from project.utils import send_mail
from architect.models import Works


# Create your views here.
@method_decorator(login_required, name='dispatch')
class BookContractorAppointmentView(View):
    def get(self,request):
        err = request.GET.get("err")
        arcs = Account.objects.filter(role='CONTRACTOR')
        return render(request,'book_contractor_appointment.html',{'err':err,'arc':arcs})
    
    def post(self,request):
        appointment_at_str = request.POST.get("appointment_at")
        appointment_for_id = request.POST.get("appointment_for")

        # Convert the appointment_at string to a datetime object
        appointment_at = timezone.make_aware(datetime.strptime(appointment_at_str, '%Y-%m-%dT%H:%M'))


        # Get the current datetime in the current timezone
        current_datetime = timezone.now()

        if appointment_at > current_datetime:
            acc = Account.objects.get(user=request.user)

            appointment_for = Account.objects.get(id=appointment_for_id)

            # check slots available for that data
            appointments_count = BookContractorAppointment.objects.filter(
                booking_date__date=appointment_at.date(),appointment_for=appointment_for
            ).count()

            if appointment_for.no_of_workers <= appointments_count:
                err = "No available Slots or Workers found!"
                return redirect(f"/contractor/book-appointment?err={err}")
            
            if not BookContractorAppointment.objects.filter(user=acc,appointment_for=appointment_for).exists():
                BookContractorAppointment.objects.create(user=acc,appointment_for=appointment_for,booking_date=appointment_at)
        else:
            err = "Please select a future datetime!"
            return redirect(f"/contractor/book-appointment?err={err}")

        msg = "Appointment Booked Successfully!"
        return redirect(f"/?msg={msg}")
    

@method_decorator(login_required, name='dispatch')
class ConHomeView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.role != 'CONTRACTOR':
            msg = "You don't have access to this page!"
            return redirect(f"/?msg={msg}")
        
        return render(request,'contractor_dash.html')
    

@method_decorator(login_required,name='dispatch')
class ConAppoitmentView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        if acc.role != 'CONTRACTOR':
            msg = "You don't have access to this page!"
            return redirect(f"/?msg={msg}")
        
        type_ = request.GET.get("type","new")
        if type_ == "new":
            appointments = BookContractorAppointment.objects.filter(appointment_for__user=request.user
                                                                    ,status=BookContractorAppointment.RECEIVED).order_by('-id')
        else:
            appointments = BookContractorAppointment.objects.filter(appointment_for__user=request.user).order_by('-id')

        return render(request,'contractor_appointments.html',{'appointments':appointments})
    

@method_decorator(login_required,name='dispatch')
class ConAcceptAppoitmentView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.role != 'CONTRACTOR':
            msg = "You don't have access to this page!"
            return redirect(f"/?msg={msg}")
        
        appointment = BookContractorAppointment.objects.get(id=id)
        appointment.status = BookContractorAppointment.ACCEPTED
        appointment.save()
        # sending email noti
        to_email = appointment.user.email
        if to_email:
            subject = "Contractor Appointment Accepted!"
            content = f"Hello {appointment.user.first_name},\nYour appointment for {appointment.appointment_for.first_name} has been approved.\n\nThanks"

            send_mail(to_email,subject,content)
        return redirect("/contractor/appointments")
    

@method_decorator(login_required,name='dispatch')
class ConRejectAppoitmentView(View):
    def get(self,request,id=None):
        acc = Account.objects.get(user=request.user)
        if acc.role != 'CONTRACTOR':
            msg = "You don't have access to this page!"
            return redirect(f"/?msg={msg}")
        
        appointment = BookContractorAppointment.objects.get(id=id)
        appointment.status = BookContractorAppointment.REJECTED
        appointment.save()
        # sending email noti
        to_email = appointment.user.email
        if to_email:
            subject = "Contractor Appointment Rejected!"
            content = f"Hello {appointment.user.first_name},\nYour appointment for {appointment.appointment_for.first_name} has been rejected.\n\nThanks"

            send_mail(to_email,subject,content)
        return redirect("/contractor/appointments")
    

@method_decorator(login_required,name='dispatch')
class ConWorksView(View):
    def get(self,request):
        works = Works.objects.filter(user__user=request.user).order_by('-id')
        return render(request,'con_works.html',{'works':works})
    

@method_decorator(login_required,name='dispatch')
class ConAddWorkView(View):
    def get(self,request):
        return render(request,"con_add_work.html")
    
    def post(self,request):
        cover = request.FILES.get("cover")
        desc = request.POST.get("desc")

        acc = Account.objects.get(user=request.user)
        Works.objects.create(cover=cover,desc=desc,user=acc)
        return redirect("/contractor/works")
    


@method_decorator(login_required,name='dispatch')
class ConWorksDeleteView(View):
    def get(self,request,id):
        Works.objects.filter(user__user=request.user,id=id).delete()
        return redirect("/contractor/works")