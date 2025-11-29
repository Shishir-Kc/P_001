"""
URL configuration for Shree_Rastriya_Secondary_School project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from . import settings 
from django.conf.urls.static import static

handler404 = 'login.views.error_404' 

app_name = 'Shree_Rastriya_secondary_School'

urlpatterns = [
    path('admin/', admin.site.urls,name="admin_profile"),
    path('accounts/login/',include('login.urls'),name="login"),
    path('',include('Home.urls'),name="home"),
    path('student/',include("student.urls"),name="student"),
    path('teacher/',include("teacher.urls"),name="teacher_dashboard"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

