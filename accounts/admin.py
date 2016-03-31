from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, Credit

admin.site.register(Teacher)

class CreditInLine(admin.TabularInline):
    model = Credit
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    inlines = [CreditInLine]

admin.site.register(Student, StudentAdmin)