from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    TYPE_STUDENT = "STUDENT"
    TYPE_PROFESSOR = "PROFESSOR"
    type = models.CharField(max_length=10)
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
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.user.get_username()

    def get_full_name(self):
        if (len(self.user.first_name) > 0) and (len(self.user.last_name) > 0):
            return self.user.get_full_name()
        else:
            return self.user.get_username()

    def create_student(*args, **kwargs):
        return User(type=UserProfile.TYPE_STUDENT, *args, **kwargs)

    def create_professor(*args, **kwargs):
        return User(type=UserProfile.TYPE_PROFESSOR, grade=0, major=0, *args, **kwargs)


class Credit(models.Model):
    student = models.ForeignKey(User)
    date = models.DateField(auto_now=True)
    CREDIT_TYPE_CHOICES = [
        (0, '竞赛获奖'),
        (1, '学术论文'),
        (2, '国家发明专利'),
        (3, '大学生创新项目'),
    ]
    credit_type = models.IntegerField('认定类型', choices=CREDIT_TYPE_CHOICES)
    value = models.IntegerField('认定学分')
    name = models.CharField('名称', max_length=300)

    def save(self, *args, **kwargs):
        if self.student.UserProfile.type != UserProfile.TYPE_STUDENT:
            return  # Yoko shall never have her own blog!
        else:
            super(Credit, self).save(*args, **kwargs)
