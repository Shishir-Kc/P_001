from django.db import models
from django.contrib.auth.models import User
from student.code import generate_unique_code


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20,default='N/A')
    last_name = models.CharField(max_length=20,default='N/A')
    contact = models.IntegerField()
    subject = models.ManyToManyField('data_class.Subject')
    teacher_class = models.ManyToManyField('data_class.Class',related_name="class_teacher",verbose_name="teacher_assigned_class")
    email = models.EmailField(("Email Address"), max_length=254,  default="Teacher@gmail.com" )
    experience = models.IntegerField(default=0)
    head_teacher = models.OneToOneField(
    'data_class.Class',
    on_delete=models.CASCADE,
    related_name="head_teacher",
    null=True,
    blank=True
)
    teacher_code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_unique_code,
        editable=True,
        verbose_name="teacher_Code",
    
    )
    teacher_image = models.ImageField(upload_to='teacher_image/',blank=True,null=True)
    refrence_code = models.CharField(verbose_name='refrence_code',default='n?A')
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Teacher_Account'
        verbose_name_plural = "Teacher_Accounts"


