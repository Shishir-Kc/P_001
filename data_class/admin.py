from django.contrib import admin
from . import models

admin.site.register(models.Class)

admin.site.register(models.Subject)

admin.site.register(models.Assignments)

admin.site.register(models.Project)


admin.site.register(models.Attendance)