from django.urls import path
from .views import *

urlpatterns = [
    path('',ArcView.as_view()),
    path('book-appointment/<int:id>',BookArchAppointmentView.as_view()),
    path('view-works/<int:id>',ViewWorksView.as_view()),
    path('buy-plans/<int:id>',BuyPlanView.as_view()),
]