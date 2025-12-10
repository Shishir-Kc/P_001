from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student.models import Student_info
from teacher.models import Teacher
from django.contrib.auth.models import User,Group
from .utils import does_user_exists
from .models import Login_Background_image


def user_login(request):
    if request.method == "POST":
        user_code = request.POST.get('user_code')
        user_pass = request.POST.get('user_pass')

        # Refactored login logic
        user = None
        
        # 1. Try to authenticate with email if provided
        if "@" in user_code:
            try:
                logging_user = User.objects.get(email=user_code)
                user = authenticate(username=logging_user.username, password=user_pass)
            except User.DoesNotExist:
                # Email not found
                pass

        # 2. If not authenticated by email, try by student/teacher code
        if user is None:
            try:
                # Try Student first
                student = Student_info.objects.select_related('user').get(student_code=user_code)
                user = authenticate(username=student.user.username, password=user_pass)
            except Student_info.DoesNotExist:
                try:
                    # Try Teacher
                    teacher = Teacher.objects.select_related('user').get(teacher_code=user_code)
                    user = authenticate(username=teacher.user.username, password=user_pass)
                except Teacher.DoesNotExist:
                    pass
        
        # 3. Final check
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            
            if user.groups.filter(name='Student').exists():
                return redirect("student:student_dashboard")
            elif user.groups.filter(name='Teacher').exists():
                return redirect("teacher:teacher_dashboard")
            else:
                 # Fallback for admin or other users
                 return redirect("home:home") # Or admin dashboard
        else:
            messages.error(request, 'Invalid credentials! Please check your email/code and password.')
            return redirect('login:login')
    
    background_image = Login_Background_image.objects.first()
    context = {
        'background_image': background_image
    }
    return render(request, 'login/login.html', context)




def user_signup(request):
   if request.method == "POST":
     email = request.POST.get('email')
     first_name = request.POST.get('first_name')
     last_name = request.POST.get('last_name')
     password = request.POST.get('user_pass')
     refrence_code = request.POST.get('reference_code')
     if not refrence_code:
         messages.error(request,'Must Provide Refrence Code !')
         return redirect('login:login')

     gender = request.POST.get('gender')
 
     user_name = first_name+' '+last_name
     if does_user_exists(email=email): 
        messages.error(request,'User with that email already exists !')


     else:
        user_account = User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password)
        user_account.save()
        group = Group.objects.get(name='Student')  
        user_account.groups.add(group)
        user_std_account = Student_info.objects.create(user=User.objects.get(username=user_name),first_name=first_name,last_name=last_name,email=email,refrence_code=refrence_code,Gender=gender)
        user_std_account.save()
        messages.success(request,'You will have Acess To Your Account in a Short Period of time ! ')
        return redirect("login:login")

   return redirect('login:login')
      


@login_required
def user_logout(request):
   
   logout(request)
   return redirect("login:login")


def error_404(request,exception):
   return render(request,'error_404/404.html',status=404)


    
    