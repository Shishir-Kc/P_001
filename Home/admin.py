from django.contrib import admin
from . import models


# Custom admin branding
admin.site.site_header = "Shree Rastriya Secondary School Admin Site"
admin.site.site_title = "Shree Rastriya Secondary School Admin Portal"
admin.site.index_title = "Welcome to Shree Rastriya Secondary School Admin Dashboard"


# Register your models here.

# tile
admin.site.register(models.Header)
# slide show

admin.site.register(models.Principal)

admin.site.register(models.Slider)

admin.site.register(models.News)

admin.site.register(models.Event)

admin.site.register(models.GalleryImage)


admin.site.register(models.Academics)

admin.site.register(models.Faculty_Teacher_Info)

admin.site.register(models.Academic_resources)

admin.site.register(models.Contact)

admin.site.register(models.Members)

admin.site.register(models.Faculty)

admin.site.register(models.Member_Role)

admin.site.register(models.Achievements_stats)

admin.site.register(models.Student_Reviews)


admin.site.register(models.Sports_Achivements)

admin.site.register(models.Academic_Achivements)

admin.site.register(models.Time_Line)

admin.site.register(models.Important_Dates)