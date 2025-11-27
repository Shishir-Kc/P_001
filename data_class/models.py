from django.db import models
from teacher import models as TD
from Home import models as HD
from teacher.utils import get_date,get_month,get_year,get_day

""""
    AUTHOR - MRC ! 


"""

class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="Subject Name")

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class Class(models.Model):

    grade = models.CharField(verbose_name="Grade/Class")
    section = models.CharField(max_length=30, verbose_name="Section",blank=True,null=True)
    faculty = models.ForeignKey(HD.Faculty,on_delete=models.CASCADE,default=1)
    subjects = models.ManyToManyField(Subject, verbose_name="Subjects")
    class_image = models.ImageField(upload_to='class_image/',blank=True,verbose_name="class_image")
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
   

    def __str__(self):

        return f"Grade = {self.grade}  Section = {self.section} Faculty = {self.faculty}"
    

class Assignments(models.Model):
    
    teacher = models.ForeignKey(TD.Teacher, on_delete=models.CASCADE,related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classs = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='notes_pdfs', null=True, blank=True)

    class Meta:
        verbose_name = "Assigment"
        verbose_name_plural = "Assigments"
        

    def __str__(self):
        return f"{self.title} - {self.classs} - {self.subject}"
    
    

class Project(models.Model):
    STATUS = [
        ('Approved','Approved'),
        ('Pending','Pending'),
        ('Rejected','Rejected'),

    ]
    student = models.ForeignKey('student.Student_info',on_delete=models.CASCADE,related_name="project")
    classs = models.ForeignKey(Class,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name="project title")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(verbose_name="Project content")
    description = models.CharField(verbose_name="description",default="N/A")
    teacher_message = models.TextField(verbose_name='message form teacher',blank=True,null=True)
    status = models.CharField(choices=STATUS,verbose_name="Project Status",default="Pending")

    class Meta:
        verbose_name = "project"

    def __str__(self):
      return f"submitted by {self.student} {self.classs.grade} {self.classs.section} | Status {self.status}"
 




class Attendance(models.Model): # need to make it uneditabe !
    year = models.CharField(max_length=4,default=get_year,verbose_name='Year')
    month = models.CharField(max_length=20,default=get_month,verbose_name='Month')
    date = models.CharField(max_length=2,default=get_date,verbose_name='Date')
    day = models.CharField(max_length=10,default=get_day)
    class Meta:
        unique_together = ('year','month','date')
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
    def __str__(self):
        return f"{self.date} {self.month} {self.year}"