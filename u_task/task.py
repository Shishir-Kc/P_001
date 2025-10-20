from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(subject:str,recivers,message:str,sender:str):
    send_mail(
             subject=subject,
             message=message,
             from_email=sender,
             recipient_list=recivers,  
             fail_silently=False,
             )
    