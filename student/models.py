from django.db import models
from django.contrib.auth.models import User
from data_class.models import Class,YEAR_MONTH
from .code import generate_unique_code
import datetime


class Student_info(models.Model):
    GENDER = {
        'Male':'Male',
        'Female':'Female'
    }
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name = "Associated_Student",related_name="student")
    student_code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_unique_code,
        editable=True,
        verbose_name="Student Code"
    )

    student_profile = models.ImageField(upload_to='student/',blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(verbose_name="student_age",blank=True,null=True)
    email = models.EmailField(verbose_name="student_email")
    Gender = models.CharField(choices=GENDER,verbose_name='Gender',blank=True,null=True)
    student_class = models.ForeignKey(Class,on_delete=models.CASCADE,verbose_name="student_class",null=True,blank=True)
    Roll_num = models.IntegerField(verbose_name="student_roll number",default=0,null=True,blank=True)
    refrence_code = models.CharField(verbose_name='refrence_code',default='n?A')
    joined = models.BooleanField(default=False,blank=True,null=True)

    # parent information ! 

    father_name = models.CharField(verbose_name='father_name',blank=True,null=True)
    mother_name = models.CharField(verbose_name='mother_name',blank=True,null=True)
    parent_contact = models.IntegerField(verbose_name='contact',blank=True,null=True)
    parent_email = models.EmailField(verbose_name='parent_email',blank=True,null=True)
    address  = models.TextField(verbose_name='Address',blank=True,null=True)
    emergency_contact = models.IntegerField(verbose_name='emergency conmtact',blank=True,null=True)



    class Meta:
        verbose_name = "student_info" 

    def __str__(self):
        return self.first_name  + " " +self.last_name




def get_today_date():

    return datetime.date.today()


class Attendence(models.Model):
    student = models.ForeignKey(Student_info, on_delete=models.CASCADE,related_name='attendence')
    attendence = models.ForeignKey(YEAR_MONTH, on_delete=models.CASCADE,verbose_name='Month/Year')
    date_month = models.DateField(default=get_today_date, blank=True,verbose_name='Month/Date') 
    attended_class = models.BooleanField(verbose_name='class_attended')

    class Meta:
        verbose_name = 'attendence'
        constraints = [
            models.UniqueConstraint(fields=['student', 'date_month'], name='unique_student_date')
        ]

    def __str__(self):
        attended = 'YES' if self.attended_class else 'NO'
        return f"{self.student.first_name} |  {self.date_month} |  PRESENT => {attended}"
