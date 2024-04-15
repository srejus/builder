from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('signup',SignupView.as_view()),
    path('profile',ProfileView.as_view(),name='edit_profile'),
    path('profile/<int:id>',ProfileView.as_view(),name='edit_user'),
    
    path('logout',LogoutView.as_view()),
]