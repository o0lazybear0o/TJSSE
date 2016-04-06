from django.contrib import admin

from project.models import Project, ProjectType, Project_Student, Document


# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectType)
admin.site.register(Project_Student)
admin.site.register(Document)