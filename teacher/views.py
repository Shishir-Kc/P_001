from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import models
from student import models as std
from data_class.models import Project, Assignments, Class, Subject,Attendance
from django.contrib import messages
from django.contrib.auth import logout
from u_task.task import send_note_upload_email
from student import models as stu
from Home import models as H
from .utils import (is_today_date_created,
get_date,
get_year,
get_month,
number_of_absent_students,
number_of_present_students,
get_todays_date,
total_days_absent,
total_days_present,
calculate_attendance_percentage,
is_attendance_taken)


@login_required
def teacher_dashboard(request):
        
        if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')

        # Optimize: Fetch teacher once. 
        # Use select_related/prefetch_related if needed.
        teacher_content = models.Teacher.objects.prefetch_related('teacher_class', 'subject').get(user=request.user)
        
        # Optimize: Use the fetched teacher object directly
        teacher_classes = teacher_content.teacher_class.all()
        
        # Optimize: distinct() might be needed if multiple classes point to same student (unlikely but safe)
        total_students = std.Student_info.objects.filter(
            student_class__in=teacher_classes
        ).count()

        students = std.Student_info.objects.filter(refrence_code = teacher_content.refrence_code)
        print(students)
      
        projects = Project.objects.filter(
            classs__in=teacher_classes, subject__in=teacher_content.subject.all()
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
        teacher_name= teacher.first_name + teacher.last_name
        students = stu.Student_info.objects.filter(
            student_class__in=teacher.teacher_class.all()
        )
        student_email = []

        for i in students:
            student_email.append(i.email)


        send_note_upload_email.delay(teacher_name=str(teacher_name),message='hi',subject=str(subject),students_emails=student_email)

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
            print("=======================")
            print(notify)
            
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
             print('================================')
             print(list_std)
            #  send_email.delay(subject=title,recivers=list_std,message=full_message,sender=teacher.email)
            
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
        
        # Handle Search
        query = request.GET.get('q')
        if query:
            from django.db.models import Q
            gallery = gallery.filter(
                Q(title__icontains=query) | 
                Q(category__icontains=query)
            )
        
        # Handle Category Filter
        category = request.GET.get('category')
        if category and category != 'all':
            gallery = gallery.filter(category=category)
            
        # Handle Pagination
        from django.core.paginator import Paginator
        paginator = Paginator(gallery, 12) # Show 12 images per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        teacher_data = models.Teacher.objects.get(user=request.user)
        context = {
            "images": page_obj, 
            "teacher": teacher_data,
            "query": query,
            "current_category": category,
        }

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
    if not student.refrence_code == teacher.refrence_code:
        messages.error(request,'Cannot edit details of student other then your own class ! ')
        return redirect("teacher:manage_std")
    
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
            messages.error(request, 'Error updating student: Add proper record ! ')
    
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
    


 
@login_required
def student_attendance_list(request):
    is_today_date_created()
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    teacher = models.Teacher.objects.get(user=request.user)
    
    # Base queryset
    students = std.Student_info.objects.filter(refrence_code=teacher.refrence_code,joined=True).order_by('Roll_num')
    
    # Calculate stats on the full list (before search/pagination)
    absent_count = number_of_absent_students(student_obj=students)
    present_count = number_of_present_students(student_obj=students)
    
    # Handle Search
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        students = students.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(Roll_num__icontains=query)
        )

    # Handle Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(students, 20) # Show 20 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    attendance = Attendance.objects.get(year=get_year(),month=get_month(),date=get_date())
    attended_std = std.Student_Attendance.objects.filter(attendance=attendance)
    attendance_dict = {}
    for atd_student in  attended_std:
         attendance_dict[atd_student.student.id] = True
         
    context =  {
        'teacher':teacher,
        'students':page_obj, # Pass page_obj instead of full list
        'absent_students' : absent_count,
        'present_students': present_count,
        'attendance_dict': attendance_dict,
        'today_date': get_todays_date(),
        'query': query,
    }
 
    return render(request,'std_attendance/student_list.html',context)

@login_required
def student_attendance_info(request,pk):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    
    # Calendar Logic
    import nepali_datetime
    from .utils import get_calendar_data # Import shared utility

    # Use shared utility
    calendar_data = get_calendar_data(get_year(), get_month(), pk)

    # Fetch records for summary stats if needed separately, or rely on utility.
    # The context needs 'student_records' list.
    try:
        attendance_objs = Attendance.objects.filter(year=get_year(),month=get_month()).order_by('date')
        student_records = std.Student_Attendance.objects.filter(student=pk,attendance__in=attendance_objs).order_by('attendance__date')
    except Exception:
        student_records = []

    teacher = models.Teacher.objects.get(user=request.user)
    student = std.Student_info.objects.get(id=pk)

    context = {
            'teacher':teacher,
            'student':student,
            'current_month': get_month(),
            'current_year':get_year(),
            'student_records':student_records,
            'calendar_data': calendar_data,
            'prefix_range': [], # Not needed with new utility structure, but keeping for template compatibility if it checks it.
                                # Actually, the new utility puts empty slots in calendar_data directly.
                                # If template iterates calendar_data, it's fine.
            'present_count': total_days_present(student_id=pk),
            'absent_count': total_days_absent(student_id=pk),
            'attendance_rate':calculate_attendance_percentage(student_id=pk),
            'is_attendance_taken':is_attendance_taken(student_id=pk),
        }
    return render(request,'std_attendance/attendance.html',context)

# to save std attendance !
@login_required
def save_attendance(request,pk):
    if not request.user.groups.filter(name='Teacher').exists():
         return redirect('home:home')
    
    if request.method == "POST":
        attended = request.POST.get('attended_class') 

        student_detail = std.Student_info.objects.get(id=pk)
        try:
            attendance = Attendance.objects.get(year=get_year(),month=get_month(),date=get_date())
        except Attendance.DoesNotExist:
            Attendance.objects.create(year=get_year(),month=get_month(),date=get_date())

        try:  
         student_attendance = std.Student_Attendance.objects.create(
            attendance = attendance,
            student = student_detail,
            attended  = attended
            )
         student_attendance.save()  
         messages.success(request,'Student attendance has been saved  !')
        except Exception as e:
            print(e)
            messages.error(request,f'{e}')
            return redirect("teacher:student_attendance_list")
        
        return redirect('teacher:student_attendance_list')
    else:
         return redirect('teacher:student_attendance_list')