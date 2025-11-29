from django.urls import path
from . import views
from student import views as sd
from teacher import views as td


app_name="home"
urlpatterns = [
    path('home/',views.home,name="home"),
    path('',views.home,name="home"),
    path('academics/',views.academics,name="academic"),
    path('admission/',views.admission,name="admission"),
    path('news/',views.news,name="news"),
    path('gallery',views.gallery,name="gallery"),
    path('achivement/',views.achivement,name="achivement"),
    path('contact/',views.contact,name="contact"),
    path('student/',sd.student_dashboard,name="dashboard"),
    path('teacher/',td.teacher_dashboard,name="teach_dash"),
    path('shared/<str:pk>/view/',views.detail_news,name='detailed_news'),   

]
