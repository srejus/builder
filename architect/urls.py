from django.urls import path
from .views import *

urlpatterns = [
    path('',ArcView.as_view()),
    path('dashboard',ArcDashView.as_view()),
    path('book-appointment/<int:id>',BookArchAppointmentView.as_view()),
    path('view-works/<int:id>',ViewWorksView.as_view()),
    path('buy-plans/<int:id>',BuyPlanView.as_view()),

    path('appointments',ArcAppointmentView.as_view()),
    path('appointments/accept/<int:id>',ArcAppointmentAcceptView.as_view()),
    path('appointments/reject/<int:id>',ArcAppointmentRejectView.as_view()),

    path('plans',ArcPlansView.as_view()),
    path('plans/add',ArcAddPlanView.as_view()),
    path('plans/delete/<int:id>',ArcPlanDeleteView.as_view()),
]