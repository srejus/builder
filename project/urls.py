from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/',include('accounts.urls')),
    path('architect/',include('architect.urls')),
    path('contractor/',include('contractor.urls')),

    path('adminuser/',include('adminuser.urls')),

]
