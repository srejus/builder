from django.urls import path
from .views import *

urlpatterns = [
    path('book-appointment',BookContractorAppointmentView.as_view()),

    path('',ConHomeView.as_view()),
    path('appointments',ConAppoitmentView.as_view()),
    path('appointments/reject/<int:id>',ConRejectAppoitmentView.as_view()),
    path('appointments/accept/<int:id>',ConAcceptAppoitmentView.as_view()),
]