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
from project.models import Project, ProjectType


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

@login_required(login_url='/accounts/login/')
def change_project_status(request, id= 0, status=7):
    id = int(id)
    status = int(status)
    if id != 0:
        which_project = ProjectType.objects.filter(id=id)
        if which_project.__len__() == 0:
            return HttpResponseRedirect(reverse('home'))
        else:
            which_project = ProjectType.objects.get(id=id)
    if not request.user.is_superuser or status > 7 or status < 0:
        return HttpResponseRedirect(reverse('home'))
    all_type = ProjectType.objects.filter(isopening=True)
    try:
        if id is 0:
            if status is 7:
                project_list = Project.objects.all()
            else:
                project_list = Project.objects.filter(status=status)
        else:
            if status is 7:
                project_list = Project.objects.filter(project_type=which_project)
            else:
                project_list = Project.objects.filter(project_type=which_project, status=status)
        return render(request, 'adminweb_change_project_status.html', {'project_list': project_list, 'all_type': all_type})
    except:
        return HttpResponseRedirect(reverse('home'))


@login_required(login_url='/accounts/login/')
def super_delete_project(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    try:
        project = Project.objects.get(id=int(id))
        project.delete()
        return HttpResponseRedirect(reverse('change_project_status', kwargs={'id': 0, 'status': 7}))
    except:
        return HttpResponseRedirect(reverse('home'))


@login_required(login_url='/accounts/login/')
def super_edit_project(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        project = Project.objects.get(id=int(id))
        project_student_list = project.project_student_set.all()
        attr = {
            'project_status': project.status,
            }
        form = forms.SuperEditProjectForm(initial=attr)
        return render(request, 'adminweb_edit_project.html', {'form': form, 'project': project, 'student_list': project_student_list})
    else:
        form = forms.SuperEditProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.get(id=int(id))
            project_student_list = project.project_student_set.all()
            project_status = request.POST.get('project_status', '')
            project.status = project_status
            project.save()
            return render(request, 'adminweb_edit_project.html',
                          {'form': form, 'project': project, 'student_list': project_student_list,  'success': True})
        return render(request, 'adminweb_edit_project.html',
                      {'form': form, 'not_valid': True})


@login_required(login_url='/accounts/login/')
def change_credit_status(request, status=3):
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
        return HttpResponseRedirect(reverse('change_credit_status', kwargs={'status': 3}))
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
