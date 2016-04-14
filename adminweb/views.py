import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import time
from accounts.models import UserProfile, Credit
from adminweb import forms


@login_required()
def home(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("../info")
    return render(request, 'base_adminweb.html')


@login_required
def new_student(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("../../info")
    if request.method == 'GET':
        form = forms.NewStudent()
        return render(request, 'adminweb_newstudent.html', {'form': form, })
    else:
        form = forms.NewStudent(request.POST)
        if form.is_valid():
            start_id = request.POST.get('start_id', '')
            end_id = request.POST.get('end_id', '')
            password = request.POST.get('password', '')
            if start_id == '':
                return render(request, 'adminweb_newstudent.html', {'form': form, 'wrong_start_id': True})
            if end_id == '':
                return render(request, 'adminweb_newstudent.html', {'form': form, 'wrong_end_id': True})
            if password == '':
                return render(request, 'adminweb_newstudent.html', {'form': form, 'wrong_password': True})
            id1 = int(start_id)
            id2 = int(end_id)
            for x in range(id1, id2 + 1):
                if User.objects.filter(username=x).__len__() == 0:

                    user = User.objects.create(username=x,)

                    user.set_password(password)
                    user.save()
                    userProfile = UserProfile.objects.create(user=user, type=UserProfile.TYPE_STUDENT)
                    userProfile.save()
            return render(request, 'adminweb_newstudent.html', {'form': form, 'success': True})
        else:
            return render(request, 'adminweb_newstudent.html', {'form': form})


@login_required
def new_professor(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect("../../info")
    if request.method == 'GET':
        form = forms.NewProfessor()
        return render(request, 'adminweb_newprofessor.html', {'form': form, })
    else:
        form = forms.NewProfessor(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            check = request.POST.get('is_superuser', '')
            if username == '':
                return render(request, 'adminweb_newprofessor.html', {'form': form, 'wrong_username': True})
            if password == '':
                return render(request, 'adminweb_newprofessor.html', {'form': form, 'wrong_password': True})
            if check == 'on':
                is_superuser = True
            else:
                is_superuser = False
            user = User.objects.create(username=username, is_superuser=is_superuser)
            user.set_password(password)
            user.save()
            userProfile = UserProfile.objects.create(user=user, type='PROFESSOR')
            userProfile.save()
            return render(request, 'adminweb_newprofessor.html', {'form': form, 'success': True})
        else:
            return render(request, 'adminweb_newprofessor.html', {'form': form})


def project_type(request):
    return render(request, 'adminweb_projecttype.html')


def new_news(request):
    return render(request, 'adminweb_newnews.html')


def change_project_status(request):
    return render(request, 'adminweb_changeprojectstatus.html')


def change_credit_statu(request, status=3):
    status = int(status)
    if not request.user.is_superuser or status > 3 or status < 0:
        return HttpResponseRedirect(reverse('home'))

    try:
        if status is 3:
            credit_list = Credit.objects.all()
        else:
            credit_list = Credit.objects.filter(status=status)
        return render(request, 'adminweb_change_credit_status.html', {'credit_list': credit_list})
    except:
        return HttpResponseRedirect(reverse('home'))


@login_required(login_url='/accounts/login/')
def super_delete_credit(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    try:
        now_credit = Credit.objects.get(id=int(id))
        now_credit.delete()
        return HttpResponseRedirect(reverse('change_credit_stauts', kwargs={'status': 3}))
    except:
        return HttpResponseRedirect(reverse('home'))


@login_required(login_url='/accounts/login/')
def super_edit_credit(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        credit = Credit.objects.get(id=int(id))
        form = forms.SuperEditCreditForm({
            'credit_type': credit.credit_type,
            'credit_second_type': credit.credit_second_type,
            'credit_third_type': credit.credit_third_type,
            'get_project_date': credit.create_credit_date,
            'credit_name': credit.name,
            'value': credit.value,
            'grade': credit.grade,
            'status': credit.status
        })
        return render(request, 'adminweb_edit_credit.html', {'form': form})
    else:
        form = forms.SuperEditCreditForm(request.POST)
        if form.is_valid():
            credit = Credit.objects.get(id=int(id))
            credit.credit_type = int(request.POST.get("credit_type", 0))
            credit.credit_second_type = int(request.POST.get("credit_second_type", 11))
            credit.credit_third_type = int(request.POST.get("credit_third_type", 11))
            credit.get_project_date = super_format_date(str(request.POST.get("get_project_date")))
            credit.name = request.POST.get("credit_name", "")
            credit.value = int(request.POST.get("value", 0))
            credit.status = int(request.POST.get("status", 0))
            credit.grade = int(request.POST.get("grade", 0))
            credit.save()
            return render(request, 'adminweb_edit_credit.html', {'form': form, 'success': "修改成功"})
        else:
            return render(request, 'adminweb_edit_credit.html', {'form': form})


def get_student_credit(request, id, status):
    status = int(status)
    if not request.user.is_superuser or status > 3 or status < 0:
        return HttpResponseRedirect(reverse('home'))

    try:
        now_student = User.objects.get(id=int(id))
        credit_list = Credit.objects.filter(student=now_student)
        if status < 3:
            credit_list = credit_list.filter(status=status)
        return render(request, 'adminweb_change_credit_status.html', {'credit_list': credit_list})
    except:
        return HttpResponseRedirect(reverse('home'))


def super_format_date(date_str):
    try:
        date_list = time.strptime(str(date_str), '%Y-%m-%d')
    except:
        date_list = time.strptime(str(date_str), '%m/%d/%Y')
    year, month, day = date_list[0:3]
    return str(datetime.date(year, month, day))
