from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
class CustomUser(User):
    def get_username(self):
        if (len(self.first_name) == 0) or (len(self.last_name) == 0):
            return self.username
        else :
            return self.last_name + ' ' + self.first_name

    def has_perm(self,permission):
        if self.is_superuser == True:
            return True

        permlist = self.perm.all()
        for perm in permlist:
            if perm.name == permission:
                return True

        grouplist = self.cgroup.all()
        for group in grouplist:
            permlist = group.perm.all()
            for perm in permlist:
                if perm.name == permission:
                    return True

        return False

class Student(CustomUser):
    grade = models.IntegerField()
    MAJOR_CHOICES = [
        (0, '暂无'),
        (1, '软件技术与管理'),
        (2, '网络与主机软件'),
        (3, '嵌入式软件与系统'),
        (4, '数字媒体'),
        (5, '其他')
    ]
    major = models.IntegerField(choices=MAJOR_CHOICES, default=0)

class Teacher(CustomUser):
    phone = models.CharField(max_length=11)

class Credit(models.Model):
    student = models.ForeignKey(Student)
    date = models.DateField(auto_now=True)
    CREDIT_TYPE_CHOICES = [
        (0, '竞赛获奖'),
        (1, '学术论文'),
        (2, '国家发明专利'),
        (3, '大学生创新项目'),
    ]
    credit_type = models.IntegerField('认定类型',choices=CREDIT_TYPE_CHOICES)
    value = models.IntegerField('认定学分')
    name = models.CharField('名称', max_length=300)