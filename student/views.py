from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . import models as std_md
from Home import models as h_mod
from data_class import models as Data
from django.contrib.auth import logout
from teacher import models as teach
from django.contrib import messages
from django.core.mail import send_mail
from teacher.views import total_class_attained_missed_this_month,filtered_month,total_days,current_month
import datetime


@login_required
def student_dashboard(request):
    if not request.user.groups.filter(name='Student').exists():
         return redirect('home:home')
        
    news=h_mod.News.objects.filter(category="Notice").order_by('-created_at')[:3]
    student_content= std_md.Student_info.objects.get(user=request.user)
    data = Data.Assignments.objects.filter(classs = student_content.student_class).order_by('-uploaded_at')[:7]
    try:
        some_data = student_content.student_class.subjects.count()
        student_section = student_content.student_class.section
    except Exception:
       some_data = 0
       student_section="Not Assigned"
    
    

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

        print('------------------------------> ')
    
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
        teacher = teach.Teacher.objects.filter(
        teacher_class=student_data.student_class,
           subject=subject).distinct()
        
        full_message = f"{full_name} has uploaded the project named : {title} \n\n Subject : {subject} \n\n Check it now !"
        email = ""
        teacher_mail = []
        for i in teacher:
           teacher_mail.append(i.email)

        send_mail(
            subject="Project submission",
            message=full_message,
            from_email= email,
            recipient_list=teacher_mail,  #
            fail_silently=False,
        )

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
    news = h_mod.News.objects.all().order_by('-created_at')
    context ={
        'new_s':news,
        'student':student,

    }
    return render(request,"news/feed.html",context)


@login_required
def student_assignment(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    student = std_md.Student_info.objects.get(user = request.user)
    data = Data.Assignments.objects.filter(classs = student.student_class).order_by('-uploaded_at')
    context = {
        'student':student,
        'assignments':data,
    }
    return render (request,'std_assignments/assignments.html',context)



@login_required
def attendence(request):
    if not request.user.groups.filter(name='Student').exists():
       return redirect('home:home')
    
    student = std_md.Student_info.objects.get(user=request.user)
    std_id = student.id
    context = {
            'teacher':teacher,
            'student':student,
            'class_attained':total_class_attained_missed_this_month(pk=std_id,type_request='attained'),
            'class_missed':total_class_attained_missed_this_month(pk=std_id,type_request='missed'),
            'total_days':total_days(),
            'current_month':current_month(date=filtered_month(date=datetime.date.today())),
        }
    return render(request,'attendence/attendence.html',context)


#  need to add delete function asap today ! 

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
       
       