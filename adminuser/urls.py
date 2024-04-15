from django.urls import path
from .views import *

urlpatterns = [
    path('',AdminHomeView.as_view()),
    path('users',AdminUserView.as_view()),
    path('users/add',AdminAddUserView.as_view()),
    path('users/delete/<int:id>',AdminDeleteUserView.as_view()),
    path('users/edit/<int:id>',AdminEditUserView.as_view()),

    path('rented-items',AdminRentedItemsView.as_view()),
    path('rented-items/restock/<int:id>',AdminRentedItemsRestockView.as_view()),
]