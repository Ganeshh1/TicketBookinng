"""TickectBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.home,name='home'),
    path('register/',views.register,name='register'), 
    path('login/',views.loginPage,name='login'),    
    path('logout/',views.logoutPage,name='logout'),    
    path('Theaters/',views.Theater_Display,name='Theater_Display'),
    path('Theaters/movies/',views.Disp,name='movies'),
    path('Theaters/movies/show/',views.Show,name='Show'),
    path('Theaters/movies/show/conform/',views.Confirm,name='Confirm'),
    path('movieadd/',views.Addmovie,name='add-movie'),
    path('movieupdate/',views.Updatemovie,name='update-movie'),
    path('removeupdate/',views.RemoveMovie,name='remove-movie'),
]


urlpatterns+=staticfiles_urlpatterns()#for static file purpose

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)#for image purpose
