from django.contrib import admin
from . import models


class Student_Admin(admin.ModelAdmin):
    list_display= [
        'first_name',
        'last_name',
        'age',
        'student_code',
        'student_class',
        'Roll_num',
        'emergency_contact',


    ]
    search_fields = [
        'age',
        'first_name',
        'last_name',
        'student_code',
        'Roll_num',
        'emergency_contact',
    ]

    list_filter=[
        'age',
        'student_class',
        'Gender',
        'joined',
    ]

   

admin.site.register(models.Student_info,Student_Admin)



class Attendence_Admin(admin.ModelAdmin):
    list_display = [ 
        'student',
        'attendence',
        'date_month',
        'attended_class',
    ]
    list_filter=[
        'attended_class',
        'date_month',
        'attendence',
        'student__student_class'
    ]

admin.site.register(models.Attendence,Attendence_Admin)