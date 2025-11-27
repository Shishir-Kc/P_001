from django.urls import path
from . import views


app_name = "teacher"
urlpatterns = [
    path('',views.teacher_dashboard,name="teacher_dashboard"),
    path('class/',views.teacher_class,name="teacher_class"),
    path('assignments/',views.student_assignments,name="assignments"),
    # path('exam/',views.exam,name="exam"),
    path('students/',views.students_list,name="student_list"),
    path('settings/',views.teacher_settings,name="settings"),    
    path('project/review/',views.student_project,name="project_submitted"),
    # path('schedule/',views.teacher_schedule,name="schedule"),
    path('upload/assignment/',views.upload_assignment,name="upload_assignment"),
    path('teacher/logout/',views.teacher_logout,name="logout"),
    path('upload/news/',views.upload_news,name="upload_news"),
    path('delete/news',views.delete_news,name="delete_news"),
    path('upload/Gallery/',views.upload_gallery,name='upload_gallery'),
    path('delete/image/',views.delete_gallery,name="delete_image"),
    path('manage/students/',views.manage_student,name='manage_std'),
    path('maanage/student/details/<uuid:pk>/',views.student_details,name='student_details'),
    path('accept/request/',views.accepet_std_request,name='accept_request'),
    path('reject/request/',views.reject_std_request,name='reject_request'),
    path('save/student/',views.edit_student,name='edit_std'),
    path('update/image/teacher/',views.update_profile_image,name="update_profile_pic"),
    path('studenet/attendance/list/',views.student_attendance_list,name='student_attendance_list'),
    path('student/<uuid:pk>/attendance/',views.student_attendance_info,name='student_attendance'),
    path('add/attendance/<uuid:pk>/',views.save_attendance,name='add_attendance')
    
]



