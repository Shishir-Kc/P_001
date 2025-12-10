from re import VERBOSE
from django.db import models
import uuid


class Header(models.Model):
    title = models.CharField(max_length=255, verbose_name="school _name")

    class Meta:
        verbose_name = "schol name"
        verbose_name_plural = "School name"

    def __str__(self):
        return self.title


class Principal(models.Model):
    name = models.CharField(verbose_name="Principal Name")
    image = models.ImageField(upload_to="principal/")
    message = models.TextField()

    class Meta:
        verbose_name = "principal"
        verbose_name_plural = "Principal"

    def __str__(self):
        return f"{self.name}"


class Slider(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="slides/")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title or f"Slide {self.id}"


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CATEGORY_CHOICES = [
        ("Academics", "Academics"),
        ("Events", "Events"),
        ("Student Life", "Student Life"),
        ("Sports", "Sports"),
        ("Announcements", "Announcements"),
        ("Notice", "Notice"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, default="School News"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notify = models.BooleanField(default=False)
    file = models.FileField(upload_to="supporting/files", blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "News"

    def __str__(self):
        return f"{self.title} | Category = > {self.category} | "


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    category = models.CharField(max_length=100, default="Academic Event")
    date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    CATEGORY = [
        ("Events", "Events"),
        ("Activities", "Activities"),
        ("Achievements", "Achievements"),
        ("Sports", "Sports"),
        ("Student Life", "Student Life"),
        ("Academics", "Academics"),
        ("Announcements", "Announcements"),
    ]
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY, default="Activities")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Gallery Image {self.title} |category = > {self.category} | "


class Achievements_stats(models.Model):
    student = models.IntegerField(verbose_name="No of Students ")
    teacher = models.IntegerField(verbose_name="No of Teachers")
    experience = models.IntegerField(verbose_name="experience")
    sucess_rate = models.IntegerField(verbose_name="Sucess_rate")
    Faculty = models.IntegerField(verbose_name="Number of Faculty`s", default=0)

    def __str__(self):
        return " Numbers for achivements"

    class Meta:
        verbose_name = "Achivement stats"
        verbose_name_plural = "Achivement stats"

class Sports_Achivements(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image  = models.ImageField(upload_to="sports_achivements/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sports Achivement"
        verbose_name_plural = "Sports Achivements"

    def __str__(self):
        return self.title
    



class Academic_Achivements(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image  = models.ImageField(upload_to="academic_achivements/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Academic Achivement"
        verbose_name_plural = "Academic Achivements"
    
    def __str__(self):
        return self.title

class Time_Line(models.Model):
    year = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = "Time_Line"
        verbose_name_plural = "Time_Lines"

    def __str__(self):
        return self.year

class Academics(models.Model):
    grade_low = models.ImageField(
        upload_to="grade/", null=True, verbose_name="lower grade"
    )
    low_des = models.TextField(verbose_name="Short description ", blank=False)
    grade_mid = models.ImageField(
        upload_to="grade/", null=True, verbose_name="middle grade"
    )
    mid_des = models.TextField(verbose_name="Short description ", blank=False)
    grade_high = models.ImageField(
        upload_to="grade/", null=True, verbose_name="high grade"
    )
    high_des = models.TextField(verbose_name="Short description ", blank=False)

    class Meta:
        verbose_name = "Academic Level"
        verbose_name_plural = "Academic Levels"

    def __str__(self):
        return "short info about classes ! "


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = True
        verbose_name = "Add_Faculty"
        verbose_name_plural = "Add_Faculties"

    def __str__(self):
        return self.name


class Faculty_Teacher_Info(models.Model):
    teacher_image = models.ImageField(upload_to="faculty/")
    teacher_name = models.CharField(max_length=100)
    teacher_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    teacher_description = models.TextField(verbose_name="short info about the teacher")
    teacher_subject = models.CharField(
        verbose_name="teacher_subject_names", default="not given"
    )

    class Meta:
        managed = True
        verbose_name = "Faculty_teacher_info"
        verbose_name_plural = "Faculty_teacher_infos"

    def __str__(self):
        return f"{self.teacher_name} | {self.teacher_faculty} | "


class Academic_resources(models.Model):
    academic_calendar = models.FileField(upload_to="pdf/")
    admission_guide = models.FileField(upload_to="pdf/")

    class Meta:
        db_table = ""
        managed = True
        verbose_name = "Academic_resource"
        verbose_name_plural = "Academic_resources"

    def __str__(self):
        return "here contains necessary resources for academic"


class Contact(models.Model):
    full_name = models.TextField(verbose_name="applicant_Name ")
    email = models.EmailField(verbose_name="applicant_Email")
    contact = models.IntegerField(verbose_name="applicant_contact")
    faculty = models.TextField(verbose_name="applicant_choosen_faculty")
    message = models.TextField(verbose_name="applicant_message")

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"

    def __str__(self):
        return f"admission inquerry from {self.full_name}"


class Member_Role(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Member_Role"
        verbose_name_plural = "Member_Roles"

    def __str__(self):
        return self.name


class Members(models.Model):
    member_image = models.ImageField(upload_to="member/")
    member_name = models.CharField(verbose_name="Name")
    member_contact = models.EmailField(verbose_name="Email", max_length=254)
    member_role = models.ForeignKey(
        Member_Role, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.member_name} | {self.member_contact}"


class Student_Reviews(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    review = models.TextField(verbose_name="review")
    image = models.ImageField(upload_to="review/")
    created_at = models.DateTimeField(auto_now_add=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, verbose_name="faculty"
    )
    class_of = models.IntegerField(verbose_name="class_of")

    class Meta:
        verbose_name = "Student_Review"
        verbose_name_plural = "Student_Reviews"

    def __str__(self):
        return self.name


class Important_Dates(models.Model):
    title  = models.CharField(max_length=100)
    secondary_title = models.CharField(max_length=100)
    initial_date = models.DateField()
    final_date = models.DateField()
    
    class Meta:
        verbose_name = "Important Date"
        verbose_name_plural = "Important Dates"
    
    def __str__(self):
        return self.title

