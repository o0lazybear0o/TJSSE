from django.db import models
from accounts.models import CustomUser
import datetime

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField(default=datetime.date.today)
    publisher = models.ForeignKey(CustomUser)
    content = models.CharField(max_length=2000)
    STATUS_PENDING = 0
    STATUS_FAIL = 1
    STATUS_PASS = 2
    STATUS_CHOICES = [
        (STATUS_PENDING, '待审核'),
        (STATUS_FAIL, '未通过'),
        (STATUS_PASS, '已通过'),
    ]
    status = models.IntegerField('审核状态',choices=STATUS_CHOICES)


class Attachment(models.Model):
    news = models.ForeignKey(News)
    filepath = models.FilePathField()