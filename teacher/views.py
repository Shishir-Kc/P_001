from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import models
from student import models as std
from data_class.models import Project, Assignments, Class, Subject,YEAR_MONTH
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from student import models as stu
from Home import models as H
import datetime
from .utils import is_std_data_filled,filtered_month,total_days,current_month,total_class_attained_missed_this_month

@login_required
def teacher_dashboard(request):
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')

        teacher = models.Teacher.objects.get(user=request.user)

        teacher_content = models.Teacher.objects.get(user=request.user)
        teacher_classes = teacher.teacher_class.all()
        total_students = std.Student_info.objects.filter(
            student_class__in=teacher_classes
        ).count()

        students = std.Student_info.objects.filter(refrence_code = teacher.refrence_code)
      
        projects = Project.objects.filter(
            classs__in=teacher.teacher_class.all(), subject__in=teacher.subject.all()
        ).order_by("-uploaded_at")[:4]
        context = {
            "teacher": teacher_content,
            "std_num": total_students,
            "projects": projects,
            'students':students,
        }
        return render(request, "teach_dashboard/dashboard.html", context)



@login_required
def teacher_class(request):
        
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        teacher = models.Teacher.objects.get(user=request.user)
        classes = teacher.teacher_class.all()
        context = {"teacher": teacher, "classes": classes}


        return render(request, "teacher_class/class.html", context)




@login_required
def student_assignments(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        if request.method == "POST":
            id = request.POST.get("assignment_id")
            try:
                assignments = Assignments.objects.get(id=id)
                assignments.delete()
            except Assignments.DoesNotExist:
                return redirect("teacher:assignments")

        teacher = models.Teacher.objects.get(user=request.user)
        assignments = Assignments.objects.filter(teacher=teacher).order_by(
            "-uploaded_at"
        )
        context = {
            "teacher": teacher,
            "assignments": assignments,
        }

        return render(request, "assignments/assignments.html", context)



@login_required
def upload_assignment(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        if request.method == "POST":
            title = request.POST.get("title")
            file = request.FILES.get("note_file")
            subject_raw = request.POST.get("subject")
            Classs_raw = request.POST.get("class")
            content = request.POST.get("description")
            subject = Subject.objects.get(id=subject_raw)
            classs = Class.objects.get(id=Classs_raw)

        data = Assignments(
            teacher=request.user.teacher,
            subject=subject,
            classs=classs,
            title=title,
            content=content,
            pdf_file=file,
        )
        data.save()
        teacher = models.Teacher.objects.get(user=request.user)
        email = teacher.email
        full_name = teacher.first_name + teacher.last_name
        message = content
        students = stu.Student_info.objects.filter(
            student_class__in=teacher.teacher_class.all()
        )
        student_email = []

        for i in students:
            student_email.append(i.email)

        full_message = (f""" 
    From: {full_name}\n
    Subject: New Note Uploaded for {subject}\n\n
    Dear Students,\n\n
    This is to inform you that a new note has been uploaded for the subject: *{subject}*.\n
    Please find the details below:\n\n
    {message}\n\n
    If you have any questions or need further clarification, feel free to reach out.\n\n
    Best regards,\n
    {full_name}
   """
 )

        send_mail(
            subject=f"Assignment Uploaded for : {subject}",
            message=full_message,
            from_email=email,
            recipient_list=student_email,  
            fail_silently=False,
        )

        messages.success(
            request, " Uploaded successfully! Your students can now access this note."
        )
        return redirect("teacher:assignments")




@login_required
def students_list(request):
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        teacher = models.Teacher.objects.get(user=request.user)
        student_data = std.Student_info.objects.filter(
            student_class__in=teacher.teacher_class.all()
        )
        context = {
            "teacher": teacher,
            "students": student_data,
        }
        return render(request, "students/students.html", context)


@login_required
def teacher_settings(request):

        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        if request.method == "POST":
            current_password = request.POST.get("current_password")

            if request.user.check_password(current_password):
                new_password = request.POST.get("new_password")
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Current password is incorrect.")

        teacher = models.Teacher.objects.get(user=request.user)

        context = {"teacher": teacher}
        return render(request, "settings/settings.html", context)

@login_required
def update_profile_image(request):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    if request.method == "POST":
        teacher_info = models.Teacher.objects.get(user=request.user)
        teacher_info.teacher_image = request.FILES.get('teacher_image')
        teacher_info.save()
        return redirect("teacher:teacher_dashboard")



@login_required
def student_project(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        if request.method == "POST":
            id = request.POST.get("project_id")
            action = request.POST.get("action_type")
            teacher_message = request.POST.get('rejection_reason')
        

            if action == "reject":
                status = "Rejected"
            else:
                status = "Approved"

            try:
                project_state = Project.objects.get(id=id)
                project_state.status = status
                if status != "Approved":
                    project_state.teacher_message = teacher_message

                project_state.save()
                if status == "Rejected":
                    messages.success(request, f" {status} project ")
                else:
                    messages.success(request, f" {status} project ")

            except Project.DoesNotExist:
                return HttpResponse("PROJECT NOT FOUND ! ")

        teacher = models.Teacher.objects.get(user=request.user)
        projects = Project.objects.filter(
            classs__in=teacher.teacher_class.all(), subject__in=teacher.subject.all()
        ).order_by("-uploaded_at")
        approved_projects = Project.objects.filter(
            status="Approved", subject__in=teacher.subject.all()
        ).count()
        rejected_projects = Project.objects.filter(
            status="Rejected", subject__in=teacher.subject.all()
        ).count()
        pending_projects = Project.objects.filter(
            status="Pending", subject__in=teacher.subject.all()
        ).count()
        context = {
            "projects": projects,
            "teacher": teacher,
            "approved": approved_projects,
            "rejected": rejected_projects,
            "pending": pending_projects,
        }
        return render(request, "student_project/project.html", context)


@login_required
def upload_news(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        if request.method == "POST":
            title = request.POST.get("title")
            category = request.POST.get("category")
            content = request.POST.get("content")
            image_file = request.FILES.get("image")
            supporting_file = request.FILES.get('pdf_file') 
            notify = request.POST.get('send_notification')
            teacher = models.Teacher.objects.get(user=request.user)
            
            
            if notify == "on":
             list_std = []
             student = std.Student_info.objects.all()
             for i in student:
              list_std.append(i.email)

             full_message = (f"""   
        From: {teacher.first_name} {teacher.last_name} ({teacher.email})\n
        Subject: New Notice - {title}\n\n
        Dear Students,\n\n
        A new notice has been issued under the category *{category}*.\n\n
         Title:  {title}\n\n
        {content}\n\n

        Please review this notice at your earliest convenience.\n\n
        Best regards,\n
        {teacher.first_name} {teacher.last_name} 
    """)

             send_mail(
             subject=title,
             message=full_message,
             from_email=teacher.email,
             recipient_list=list_std,  
             fail_silently=False,
             )
            

            data = H.News(
                title=title, description=content, image=image_file, category=category , file =supporting_file
            )
            data.save()
            messages.success(request, "Uploaded Sucessfully ! ")
            return redirect("teacher:upload_news")

        teacher = models.Teacher.objects.get(user=request.user)
        news = H.News.objects.all()

        context = {"teacher": teacher, "new_s": news}
        return render(request, "news_upload/news.html", context)



@login_required
def upload_gallery(request):
       
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        if request.method == "POST":

            title = request.POST.get("title")
            category = request.POST.get("category")
            image = request.FILES.get("image_file")
            data = H.GalleryImage(title=title, image=image, category=category)
            data.save()
            messages.success(request, "Image uploaded Sucessfully ! ")
            return redirect("teacher:upload_gallery")

        gallery = H.GalleryImage.objects.all()
        teacher_data = models.Teacher.objects.get(user=request.user)
        context = {"images": gallery, "teacher": teacher_data}

        return render(request, "gallery_upload/gallery.html", context)


@login_required
def delete_gallery(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        if request.method == "POST":
            id = request.POST.get("image_id")
            image_data = H.GalleryImage.objects.get(id=id)
            image_data.delete()
            messages.success(request, "Image Deleted Sucessfully ! ")
            return redirect("teacher:upload_gallery")


@login_required
def delete_news(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        if request.method == "POST":
            try:
                news_id = request.POST.get("news_id")
                news = H.News.objects.get(id=news_id)
                news.delete()
                messages.success(request, "Deleted successfully!")
            except H.News.DoesNotExist:
                messages.error(request, "News not found.")
            except Exception as e:
                messages.error(request, f"Failed to delete: {str(e)}")

            return redirect("teacher:upload_news")
        else:
            return redirect("teacher:upload_news")
    


@login_required
def teacher_logout(request):
        
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
        logout(request)
        return redirect("login:login")




@login_required
def manage_student(request):
    
        
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
    
    teacher_info = models.Teacher.objects.get(user=request.user)
    students = std.Student_info.objects.filter(refrence_code = teacher_info.refrence_code)
    total_students = std.Student_info.objects.filter(refrence_code=teacher_info.refrence_code,joined=True)
    context = {
        'students':students,
        'teacher':teacher_info,
        'totalstudents':total_students,
    }
    return render (request,'manage_std/manage_std.html',context)

@login_required
def accepet_std_request(request):
    
        
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
    if request.method == "POST":
        student = request.POST.get('student_id')
        student_info = std.Student_info.objects.get(id=student)
        teacher = models.Teacher.objects.get(user=request.user)


        student_info.student_class = teacher.head_teacher


        student_info.joined = True
        student_info.save()


    return redirect('teacher:manage_std')

@login_required
def reject_std_request(request):
    
        
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
    if request.method == "POST":
        student = request.POST.get('student_id')
        student_info = std.Student_info.objects.get(id=student)
        student_info.refrence_code = False
        student_info.student_class = None
        student_info.joined = False
        student_info.save()
        return redirect('teacher:manage_std')
        

@login_required
def student_details(request,pk):

    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
    teacher = models.Teacher.objects.get(user=request.user)

    student = std.Student_info.objects.get(id=pk)
    context = {
        'student':student,
        'teacher':teacher
    }
    return render(request,'student_details/student_detail.html',context)


@login_required
def edit_student(request):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        edit_section = request.POST.get('edit_section')  
        
        try:
            student_info = std.Student_info.objects.get(id=student_id)
            
    
            if edit_section in ['student', 'both']:
                age = request.POST.get('age')
                roll_number = request.POST.get('roll_number')
 
                if age:
                    try:
                        age_int = int(age)
                        if 5 <= age_int <= 25:
                            student_info.age = age_int
                        else:
                            messages.error(request, 'Age must be between 5 and 25.')
                            return redirect('teacher:student_details', pk=student_id)
                    except ValueError:
                        messages.error(request, 'Age must be a valid number.')
                        return redirect('teacher:student_details', pk=student_id)
                
 
                if roll_number:
                    try:
                        roll_int = int(roll_number)
                        if roll_int > 0:
                            student_info.Roll_num = roll_int
                        else:
                            messages.error(request, 'Roll number must be a positive integer.')
                            return redirect('teacher:student_details', pk=student_id)
                    except ValueError:
                        messages.error(request, 'Roll number must be a valid integer.')
                        return redirect('teacher:student_details', pk=student_id)
            
     
            if edit_section in ['parent', 'both']:
                father_name = request.POST.get('father_name')
                mother_name = request.POST.get('mother_name')
                parent_contact = request.POST.get('parent_contact')
                parent_email = request.POST.get('parent_email')
                address = request.POST.get('address')
                emergency_contact = request.POST.get('emergency_contact')
                
            
                if father_name is not None:
                    student_info.father_name = father_name
                if mother_name is not None:
                    student_info.mother_name = mother_name
                if parent_contact is not None:
                    student_info.parent_contact = parent_contact
                if parent_email is not None:
                    student_info.parent_email = parent_email
                if address is not None:
                    student_info.address = address
                if emergency_contact is not None:
                    student_info.emergency_contact = emergency_contact
            
            student_info.save()
            messages.success(request, 'Student information updated successfully!')
            
        except std.Student_info.DoesNotExist:
            messages.error(request, 'Student not found.')
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    return redirect('teacher:student_details', pk=student_id)


@login_required
def remove_student(request):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
        
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        student = std.Student_info.objects.get(id=student_id)
        student.refrence_code = "REJECTED"
        student.student_class  = None
        student.joined  = False
        student.save()

        return redirect('teacher:manage_std')
    
# @login_required
# def student_attendence (request):
    # if not request.user.groups.filter(name='Teacher').exists():
    #      return redirect('home:home')
#     teacher = models.Teacher.objects.get(user=request.user)
#     students = std.Student_info.objects.filter(refrence_code=teacher.refrence_code,)
#     dtaa = std.Attendence.objects.filter(
#         student = 1,
#         date_month = '2025-08-14',
#         attended_class = True
#     ).count()
#     print(dtaa)
    
   

#     context =  {
#         'teacher':teacher,
#         'students':students,

#     }
#     return render(request,'attendence/student_list.html',context)

# @login_required

  


def is_std_data_filled(pk):
    is_done = std.Attendence.objects.filter(
        student = pk,
        date_month = datetime.date.today(),
        ).exists()
    if is_done:
        return True
    else:
        return False

def filtered_month(date):
    month = str(date)
    filtered_month = int((month[6:][:-3]))
    return filtered_month

def total_days():
    current_month = YEAR_MONTH.objects.get(current_year=datetime.date.today().year, month=filtered_month(date=datetime.date.today()))
    data = {
        'number_of_days':current_month.number_of_days,
        'number_of_holidays':current_month.holiday,
        'number_of_unexpected_holidays':current_month.unexpected_holiday,
        }
    return data

def current_month(date):
   MONTH = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
   return MONTH.get(date,"invalid month")

def total_class_attained_missed_this_month(pk, type_request):
    student = std.Student_info.objects.get(id=pk)
    today = datetime.date.today()
    year_month_obj = YEAR_MONTH.objects.get(month=today.month, current_year=today.year)
    
    if type_request == "attained":
        dtaa = std.Attendence.objects.filter(
            student=student,
            attendence=year_month_obj,
            attended_class=True
        ).count()
        return dtaa
    
    elif type_request == "missed":
        dtaa =std.Attendence.objects.filter(
            student=student,
            attendence=year_month_obj,
            attended_class=False
        ).count()
        return dtaa
    

    
# list of all std ! 
@login_required
def student_attendence_list(request):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    teacher = models.Teacher.objects.get(user=request.user)
    students = std.Student_info.objects.filter(refrence_code=teacher.refrence_code).order_by('Roll_num')
    context =  {
        'teacher':teacher,
        'students':students,

    }
    return render(request,'std_attendence/student_list.html',context)

# to show user stact / add attendence 
@login_required
def student_add_attendence(request,pk):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    if request.method == "POST":
        teacher = models.Teacher.objects.get(user=request.user)
        student = std.Student_info.objects.get(id=pk)
        context = {
            'teacher':teacher,
            'student':student,
            'is_done':is_std_data_filled(pk),
            'class_attained':total_class_attained_missed_this_month(pk,type_request='attained'),
            'class_missed':total_class_attained_missed_this_month(pk,type_request='missed'),
            'total_days':total_days(),
            'current_month':current_month(date=filtered_month(date=datetime.date.today()))
        }
        return render(request,'std_attendence/attendence.html',context)
    else:
        teacher = models.Teacher.objects.get(user=request.user)
        student = std.Student_info.objects.get(id=pk)
        context = {
            'teacher':teacher,
            'student':student,
            'is_done':is_std_data_filled(pk),
            'class_attained':total_class_attained_missed_this_month(pk,type_request='attained'),
            'class_missed':total_class_attained_missed_this_month(pk,type_request='missed'),
            'total_days':total_days(),
            'current_month':current_month(date=filtered_month(date=datetime.date.today())),
        }
        return render(request,'std_attendence/attendence.html',context)


# to save std attendence !
@login_required
def save_attendence(request,pk):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    
    if request.method == "POST":
        student_id = pk
        attained = request.POST.get('attended_class') 
        student_detail = std.Student_info.objects.get(id=student_id)
        
        current_month = YEAR_MONTH.objects.get(current_year=datetime.date.today().year, month=filtered_month(datetime.date.today())) 
        try:  
         attendance = std.Attendence.objects.create(
         student=student_detail,
         attendence=current_month,
         date_month=datetime.date.today(),
         attended_class=attained,
         )
         attendance.save()
        except Exception:
            print("error data duplicated ! ")
            return redirect("teacher:student_attendence")
        
        return redirect('teacher:student_attendence',pk=pk)
    