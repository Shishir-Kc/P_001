from django.urls import path
from . import views


app_name = "student"
urlpatterns = [

    path('',views.student_dashboard,name="student_dashboard"),
    path('setting/',views.student_setting,name="setting"),  
    path('teacher/list',views.teacher,name="teacher"),
    # path('subject/',views.student_books,name="books"),
    path('project/',views.student_project,name="project"),
    path('news/feed/',views.student_news,name="news_feed"),
    path('view/assignments',views.student_assignment,name="assignments"),
    path('student/logout/',views.std_logout,name="std_logout"),
    path('delete/project/',views.std_project_delete,name="delete_project"),
    path('update/refrence/',views.update_refrence_code,name='update_code'),
    path('update/image/',views.update_image,name='update_image'),
    path('attendence/',views.attendence,name="attendence")

]


