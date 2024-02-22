from django.urls import path
from .views import *

urlpatterns = [
    path('',IndexView.as_view()),
    path('rent-items',RentItemsView.as_view())
]