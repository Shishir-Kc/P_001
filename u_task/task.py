from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings







@shared_task
def send_contact_mail(body:str,
                      matter_of_subject:str,
                      email:str,
                      full_name:str,
                      contact:int):

    html_content = render_to_string(
        "email/contact_mail.html",
         {
            "full_name": full_name,
            "email": email,
            "phone": contact,
            "subject": matter_of_subject,
            "message": body,
            "platform_name": settings.PLATFORM_NAME,
        },
    
    )

    msg = EmailMultiAlternatives(
        subject=matter_of_subject,
        from_email=settings.EMAIL_HOST_USER,  
        to=[email],
        headers={"List-Unsubscribe": f"<mailto:{settings.EMAIL_HOST_USER}"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_note_upload_email(students_emails:list,
                           subject:str,
                           message:str,
                           teacher_name:str
                           ):

    html_content = render_to_string(
        "email/upload_assignment_email.html",
        {
            "subject":subject,
            "teacher_name":teacher_name,
            "message":message,
            "platform_name":settings.PLATFORM_NAME
        }
    )
    
    msg = EmailMultiAlternatives(
        subject=f"New Note has been uploaded for {subject}",
        body= "" ,
        from_email=settings.EMAIL_HOST_USER,
        to = students_emails,
        headers={"List-Unsubscribe": f"<mailto:{settings.EMAIL_HOST_USER}"},
    )
    msg.attach_alternative(html_content,"text/html")
    msg.send()

@shared_task
def send_project_upload_email(teacher_email:str,
                              teacher_name:str,
                              student_name:str,
                              title:str,
                              subject:str,
                              submission_date:str,
                              ):


    html_content = render_to_string(
        'email/student_project_upload_email.html',
        {
            'teacher_name':teacher_name,
            'subject_name':subject,
            'student_name':student_name,
            'project_title':title,
            'submission_date':submission_date,
            'platform_name':settings.PLATFORM_NAME
        }
    ) 
    msg = EmailMultiAlternatives(
        subject="New Assignment Submitted",
        body=" ",
        from_email=settings.EMAIL_HOST_USER,
        to = [teacher_email],
        headers={"List-Unsubscribe": f"<mailto:{settings.EMAIL_HOST_USER}"},
    )
    try:
     msg.attach_alternative(html_content,"text/html")
     msg.send()
     return f"sucessfully sent the email ! "
    except:
       return f"failed to send !{student_name} project mail to {teacher_name}"