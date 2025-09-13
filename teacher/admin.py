from django.contrib import admin
from . import models



class Teacher_Admin(admin.ModelAdmin):
    list_display = [
        'name',
        'first_name',
        'last_name',
        'head_teacher',
        'teacher_code',
        'refrence_code',
        # 'get_subjects',
        'experience',
    ]

    # def get_subjects(self,obj):
    #     return ", ".join([s.name for s in obj.subject.all()])
    
    # get_subjects.short_description = "Subjects" 
    
    list_filter = [ 
        'experience',
        'subject',
        'teacher_class',
    ]

    search_fields = [ 
        'name',
        'first_name',
        'last_name',
        'refrence_code',
        'teacher_code',
        'teacher_class__grade',
        
    ]

admin.site.register(models.Teacher,Teacher_Admin)
