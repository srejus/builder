from django.urls import path
from .views import *

urlpatterns = [
    path('book-appointment',BookContractorAppointmentView.as_view()),
]