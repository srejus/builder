from django.urls import path
from .views import *

urlpatterns = [
    path('',IndexView.as_view()),
    path('rent-items',RentItemsView.as_view()),
    path('place-order/<int:id>',PlaceOrderView.as_view()),
    path('my-orders',MyOrdersView.as_view()),
]