from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . import models as std_md
from Home import models as h_mod
from data_class import models as Data
from django.contrib.auth import logout
from teacher import models as teach
from django.contrib import messages
from u_task.task import send_project_upload_email
from teacher.utils import (
total_days_absent,
total_days_present,
get_month,
get_year,
calculate_attendance_percentage)
from data_class.models import Attendance
from django.core.paginator import Paginator 

@login_required
def student_dashboard(request):
    if not request.user.groups.filter(name='Student').exists():
         return redirect('home:home')
        
    news = h_mod.News.objects.filter(category="Notice").order_by('-created_at')[:3]
    
    # Optimize: Use select_related for foreign keys if needed, though Student_info might not have many here.
    # Assuming Student_info -> user is OneToOne or ForeignKey
    student_content = std_md.Student_info.objects.select_related('student_class').get(user=request.user)
    
    # Optimize: Filter assignments by class directly
    data = Data.Assignments.objects.filter(classs=student_content.student_class).order_by('-uploaded_at')[:7]
    
    try:
        # Optimize: Use count() directly on the relationship if possible, but here we access student_class.subjects
        # If subjects is ManyToMany, count() is fine.
        if student_content.student_class:
             some_data = student_content.student_class.subjects.count()
             student_section = student_content.student_class.section
        else:
             some_data = 0
             student_section = "Not Assigned"
    except Exception:
       some_data = 0
       student_section = "Not Assigned"
    
    roll_num = student_content.Roll_num
    context = {
        'new_s' :news,
        'student':student_content,
        'assignments':data,
        'total_subject': some_data,
        'student_section':student_section,
        'roll_num':roll_num,
      
    }

    return render(request,"dashboard/dashboard.html",context)



@login_required
def update_image(request):
    if not request.user.groups.filter(name='Student').exists():
        return redirect('home:home')
    
    if request.method == 'POST':
        student_image = std_md.Student_info.objects.get(user=request.user)
        student_image.student_profile = request.FILES.get('profile_image')
        student_image.save()
        return redirect('student:student_dashboard')    
    




@login_required
def student_setting(request):
    
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')


    if request.method == "POST":
        current_password = request.POST.get('current_password')

        if request.user.check_password(current_password):
            new_password = request.POST.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
         
        else:
            messages.error(request,'your current password did not matched !')
            return redirect('student:setting')
    

    
    student_content= std_md.Student_info.objects.get(user=request.user)
    context = {
        'student': student_content,
    }
    return render(request,"setting/setting.html",context)




@login_required
def teacher(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
  
    student_content= std_md.Student_info.objects.get(user=request.user)
    teachers = teach.Teacher.objects.filter(teacher_class = student_content.student_class)
    context = {
        'student': student_content,
        'teachers':teachers,
    }
    return render(request,"teacher/teacher.html",context)





@login_required
def student_project(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    
    if request.method == "POST":
        title = request.POST.get('title')
        subject_id= request.POST.get('subject')
        student_content= std_md.Student_info.objects.get(user=request.user)
        file = request.FILES.get('file')
        description = request.POST.get('description')
        subject = Data.Subject.objects.get(id=subject_id)
        data = Data.Project(student=request.user.student,classs = student_content.student_class,title=title,pdf=file,description=description,subject=subject)
        data.save()
        student_data= std_md.Student_info.objects.get(user=request.user)
        full_name = student_data.first_name  + student_data.last_name
        print(subject)
        teacher = teach.Teacher.objects.get(teacher_class = student_data.student_class,subject=subject)



        """   

            this code might be use full but as of now take it as refrence

        # teacher = teach.Teacher.objects.filter(
        # teacher_class = student_data.student_class,
        #    subject=subject).distinct()
        
        # full_message = f"{full_name} has uploaded the project named : {title} \n\n Subject : {subject} \n\n Check it now !"
        
        # teacher_mail = []
        # for i in teacher:
        #    teacher_mail.append(i.email)

        """
        send_project_upload_email.delay(teacher_name = str(teacher.user.get_full_name()), teacher_email=teacher.email,student_name=full_name,title=title,subject=str(subject),submission_date=str(data.uploaded_at))
        messages.success(request,"uploaded Sucessfully ! ")
        return redirect ("student:project")

    student = std_md.Student_info.objects.get(user=request.user)
    project = Data.Project.objects.filter(student=student).order_by('-uploaded_at')

    context = { 
        'student':student,
        'projects':project,
        
    }
    return render (request,"project/project.html",context)



@login_required
def student_news(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    student = std_md.Student_info.objects.get(user = request.user)
    news_list = h_mod.News.objects.all().order_by('-created_at')

    # Handle Search
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        news_list = news_list.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Handle Category Filter
    category = request.GET.get('category')
    if category and category != 'all':
        news_list = news_list.filter(category=category)

    # Handle Pagination
    paginator = Paginator(news_list, 6) # Show 6 news items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'new_s': page_obj,
        'student': student,
        'query': query,
        'current_category': category,
    }
    return render(request,"news/feed.html",context)


@login_required
def student_assignment(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    student = std_md.Student_info.objects.get(user = request.user)
    assignments_list = Data.Assignments.objects.filter(classs = student.student_class).order_by('-uploaded_at')

    # Handle Search
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        assignments_list = assignments_list.filter(
            Q(title__icontains=query) | 
            Q(subject__name__icontains=query)
        )
    
    # Handle Subject Filter
    subject_filter = request.GET.get('subject')
    if subject_filter and subject_filter != 'all':
        assignments_list = assignments_list.filter(subject__name=subject_filter)

    # Handle Pagination
    paginator = Paginator(assignments_list, 9) # Show 9 assignments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'student':student,
        'assignments':page_obj,
        'query': query,
        'current_subject': subject_filter,
    }
    return render (request,'std_assignments/assignments.html',context)



@login_required
def attendence(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    
    student = std_md.Student_info.objects.get(user=request.user)
    import nepali_datetime
    from teacher.utils import get_calendar_data # Import shared utility

    # Use shared utility to get calendar data
    calendar_data = get_calendar_data(get_year(), get_month(), student.id)

    
    try:
        attendance_objs = Attendance.objects.filter(year=get_year(),month=get_month()).order_by('date')
        student_records = std_md.Student_Attendance.objects.filter(student=student.id,attendance__in=attendance_objs).order_by('attendance__date')
    except Exception:
        student_records = []

    context = {
            'teacher': teacher, 
            'student': student,
            'current_month': get_month(),
            'current_year': get_year(),
            'student_records': student_records,
            'calendar_data': calendar_data,
            'present_count': total_days_present(student_id=student.id),
            'absent_count': total_days_absent(student_id=student.id),
            'attendance_rate': calculate_attendance_percentage(student_id=student.id)
        }
    return render(request,'attendence/attendence.html',context)




@login_required
def std_project_delete(request):
   if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
   if request.method == "POST":
      id = request.POST.get('project_id')
      project = Data.Project.objects.get(id=id)
      project.delete()
      messages.success(request,"deleted sucessfully ! ")
      return redirect('student:project')
   else:
      messages.success(request,'unnable to do action ')
      return redirect('student:project')

  
@login_required
def std_logout(request):
 
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    logout(request)
    return redirect('login:login')


@login_required
def update_refrence_code(request):
   if not request.user.groups.filter(name='Student').exists():
      return redirect('home:home')
   student = std_md.Student_info.objects.get(user = request.user)
   
   if request.method == "POST":
        student.refrence_code = request.POST.get('reference_code')  
        student.save()
        messages.success(request,'Refrence Code Updated Waiting for Acceptence')
        return redirect('student:setting')
   else:
       
      messages.error(request,'unnable to do action ')
      return redirect('student:student_dashboard')
       
       