from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    TYPE_STUDENT = "STUDENT"
    TYPE_PROFESSOR = "PROFESSOR"
    type = models.CharField(max_length=10)
    grade = models.IntegerField(null=True)
    MAJOR_CHOICES = [
        (0, '暂无'),
        (1, '软件技术与管理'),
        (2, '网络与主机软件'),
        (3, '嵌入式软件与系统'),
        (4, '数字媒体'),
        (5, '其他')
    ]
    major = models.IntegerField(choices=MAJOR_CHOICES, default=0)
    phone = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.user.get_username()

    def get_full_name(self):
        if (len(self.user.first_name) > 0) and (len(self.user.last_name) > 0):
            return self.user.get_full_name()
        else:
            return self.user.get_username()

    def is_profile_completed(self):
        if (len(self.user.first_name) == 0) or (len(self.user.last_name) == 0) or (len(self.user.email) == 0):
            return False
        if (self.type == UserProfile.TYPE_STUDENT) and (not self.grade):
            return False
        return True

    def create_student(*args, **kwargs):
        return User(type=UserProfile.TYPE_STUDENT, *args, **kwargs)

    def create_professor(*args, **kwargs):
        return User(type=UserProfile.TYPE_PROFESSOR, grade=0, major=0, *args, **kwargs)


class Credit(models.Model):
    student = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    CREDIT_TYPE_CHOICES = [
        (1, '竞赛获奖'),
        (2, '学术论文'),
        (3, '国家发明专利'),
        (4, '大学生创新项目'),
    ]
    CREDIT_SECOND_TYPE = [
        (11, '校级'), (12, '省级'), (13, '国家级'), (14, '国际级'), (15, '其他'),
        (21, '权威报纸'), (22, '核心期刊'), (23, 'SCI/EI检索'),
        (0, '无')
    ]
    CREDIT_TYPE_THIRD = [
        (11, '一等奖'), (12, '二等奖'), (13, '三等奖'),
        (21, '第一作者'), (22, '第二作者'), (23, '第三作者'),
        (0, "无")
    ]
    credit_type = models.IntegerField('认定类型', choices=CREDIT_TYPE_CHOICES)
    credit_second_type = models.IntegerField('认定等级2', choices=CREDIT_SECOND_TYPE)
    credit_third_type = models.IntegerField('认定等级3', choices=CREDIT_TYPE_THIRD)

    CREDIT_STATUS_CHOICES = [
        (0, '待审核'),
        (1, '未通过'),
        (2, '已通过'),
    ]
    status = models.IntegerField('审核状态', choices=CREDIT_STATUS_CHOICES, default=0)

    CREDIT_GEADE = [
        (5, '优'),
        (4, '良'),
        (3, '中'),
        (2, '及格'),
        (0, '暂无')
    ]
    grade = models.IntegerField('学分等级', choices=CREDIT_GEADE, default=0)

    value = models.IntegerField('认定学分', default=0)
    name = models.CharField('名称', max_length=300)

    def save(self, *args, **kwargs):
        if self.student.userprofile.type != UserProfile.TYPE_STUDENT:
            return  # Yoko shall never have her own blog!
        else:
            super(Credit, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.student.userprofile) + " name:" + self.name + " value: " + str(self.value)

    class Meta:
        ordering = ['date']
