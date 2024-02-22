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
            if not BookContractorAppointment.objects.filter(user=acc,appointment_for=appointment_for).exists():
                BookContractorAppointment.objects.create(user=acc,appointment_for=appointment_for,booking_date=appointment_at)
        else:
            err = "Please select a future datetime!"
            return redirect(f"/contractor/book-appointment?err={err}")

        msg = "Appointment Booked Successfully!"
        return redirect(f"/?msg={msg}")