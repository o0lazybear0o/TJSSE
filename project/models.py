from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
import datetime


# Create your models here.
class ProjectType(models.Model):
    typename = models.CharField(max_length=20)

    TYPE_NATIONAL = 0
    TYPE_SHANGHAI = 1
    TYPE_SITP = 2
    TYPE_SECOLLEGE = 3
    TYPE_ELSE = 4
    TYPE_CHOICES = [
        (TYPE_NATIONAL, '国创'),
        (TYPE_SHANGHAI, '市创'),
        (TYPE_SITP, 'SITP'),
        (TYPE_SECOLLEGE, '院创'),
        (TYPE_ELSE, '其他'),
    ]
    type = models.IntegerField('认定类型',choices=TYPE_CHOICES)

    isopening = models.BooleanField('是否开放中', default=True)
    starttime = models.DateField(default=datetime.date.today)
    endtime = models.DateField()
    note = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.typename


class Project(models.Model):
    name = models.CharField(max_length=30)
    project_type = models.ForeignKey(ProjectType)
    description = models.CharField(max_length=100)
    professor = models.ForeignKey(User)

    STATUS_BEFORE_INIT = 0
    STATUS_APPLY_INIT = 1
    STATUS_COMPLETE_INIT = 2
    STATUS_APPLY_MID = 3
    STATUS_COMPLETE_MID = 4
    STATUS_APPLY_FINAL = 5
    STATUS_COMPLETE_FINAL = 6

    STATUS_CHOICES = [
        (STATUS_BEFORE_INIT, '未申请立项'),
        (STATUS_APPLY_INIT, '申请立项'),
        (STATUS_COMPLETE_INIT, '立项通过'),
        (STATUS_APPLY_MID, '申请中期'),
        (STATUS_COMPLETE_MID, '中期通过'),
        (STATUS_APPLY_FINAL, '申请结题'),
        (STATUS_COMPLETE_FINAL, '已结题'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_BEFORE_INIT)
    endtime = models.DateField(null=True)
    note = models.CharField(max_length=300, blank=True)

    def get_status(self):
        return self.STATUS_CHOICES[self.status].__getitem__(1)

    def save(self, *args, **kwargs):
        if self.professor.userprofile.type != UserProfile.TYPE_PROFESSOR:
            return # Yoko shall never have her own blog!
        else:
            super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name+', '+str(self.professor.get_username())
    __repr__=__str__


class Project_Student(models.Model):
    student = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    is_superuser = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.student.userprofile.type != UserProfile.TYPE_STUDENT:
            return # Yoko shall never have her own blog!
        else:
            super(Project_Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.student.get_username()+', '+self.project.name
    __repr__=__str__


class Document(models.Model):
    project = models.ForeignKey(Project)
    filename = models.CharField(max_length=20)

    DOCTYPE_INIT = 0
    DOCTYPE_MID = 1
    DOCTYPE_FINAL = 2
    DOCTYPE_ELSE = 3
    DOCTYPE_CHOICES = [
        (DOCTYPE_INIT, '开题文档'),
        (DOCTYPE_MID, '中期文档'),
        (DOCTYPE_FINAL, '结题文档'),
        (DOCTYPE_ELSE, '其他'),
    ]
    type = models.IntegerField('文档类型',choices=DOCTYPE_CHOICES)

    STATUS_PENDING = 0
    STATUS_FAIL = 1
    STATUS_PASS = 2
    STATUS_CHOICES = [
        (STATUS_PENDING, '待审核'),
        (STATUS_FAIL, '未通过'),
        (STATUS_PASS, '已通过'),
    ]
    status = models.IntegerField('审核状态',choices=STATUS_CHOICES)

    date = models.DateField(default=datetime.date.today)
    filepath = models.FilePathField()
    note = models.CharField(max_length=300, blank=True)


class Fund(models.Model):
    project = models.ForeignKey(Project)
    fund_type = models.CharField(max_length=60)
    value=models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    note = models.CharField(max_length=300, blank=True)