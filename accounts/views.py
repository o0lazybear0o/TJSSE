import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.sql import OR
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from project.models import Project, ProjectType, Project_Student, Fund
from django.template.context import RequestContext
from django.views import generic
from accounts import forms
from accounts.models import UserProfile, Credit
from TJSSE.utils import ExtendPaginator
from django.core.paginator import PageNotAnInteger, EmptyPage
import time


# Create your views here.
# Pag for log in
def login(request):
    if request.user.is_authenticated():
        return redirect('/accounts/info')
    else:
        if request.method == 'GET':
            form = forms.LoginForm
            return render_to_response('login.html', RequestContext(request, {'form': form, }))
        else:
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')

                if username == '':
                    return render(request, 'login.html', {'form': form, 'username_not_valid': True})
                elif password == '':
                    return render(request, 'login.html', {'form': form, 'password_not_valid': True})

                user = auth.authenticate(username=username, password=password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('../')
                else:
                    return render(request, 'login.html', {'form': form, 'password_is_wrong': True})
            else:
                return render(request, 'login.html', {'form': form, 'not_valid': True})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


# Change Password
@login_required
def change_password_view(request):
    if request.method == 'GET':
        form = forms.ChangePasswordForm
        return render(request, 'change_password.html', {'form': form, })
    else:
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            new_password_again = request.POST.get('new_password_again', '')

            if old_password == "" or new_password == "" or new_password_again == "":
                return render(request, 'change_password.html', {'form': form, 'not_valid': True})

            username = request.user.username
            user = auth.authenticate(username=username, password=old_password)

            if user is not None and user.is_active:
                if new_password != new_password_again:
                    return render(request, 'change_password.html', {'form': form, 'password_not_same': True})
                else:
                    user.set_password(new_password)
                    user.save()
                    auth.login(request, user)
                return render(request, 'change_password.html', {'form': form, 'success': True})
            else:
                return render(request, 'change_password.html', {'form': form, 'old_password_is_wrong': True})
        else:
            return render(request, 'change_password.html', {'form': form, 'not_valid': True})


@login_required(login_url='/accounts/login/')
def new_project(request):
    if request.user.userprofile.type != 'STUDENT':
        return HttpResponseRedirect('/accounts/info')
    if request.method == 'GET':
        form = forms.NewProjectForm()
        return render(request, 'new_project.html', {'form': form, })
    else:
        form = forms.NewProjectForm(request.POST)
        if form.is_valid():
            project_type_id = request.POST.get('project_type', '')
            project_name = request.POST.get('project_name', '')
            professor_id = request.POST.get('professor', '')
            partner_list = []
            for x in range(1, 5):
                partner_list.append(request.POST.get('partner' + str(x), ''))
            description = request.POST.get('description', '')
            project_type = ProjectType.objects.get(id=project_type_id)
            professor = UserProfile.objects.get(id=professor_id).user
            for x in partner_list:
                if x != '' and User.objects.filter(username=x).__len__() == 0:
                    return render(request, 'new_project.html', {'form': form, 'wrong_student_id': True})
            project = Project.objects.create(
                name=project_name,
                project_type=project_type,
                description=description,
                professor=professor,
                endtime=project_type.endtime,
            )
            project.save()
            Project_Student.objects.create(
                student=request.user,
                project=project,
                is_superuser=True,
            ).save()

            for x in partner_list:
                if x != '':
                    student = User.objects.get(username=x)
                    Project_Student.objects.create(
                        student=student,
                        project=project,
                        is_superuser=False,
                    ).save()

            return render(request, 'new_project.html', {'form': form, 'success': True})
        else:
            return render(request, 'new_project.html', {'form': form, 'not_valid': False})


# Page for user info
@login_required(login_url='/accounts/login/')
def change_user_info_view(request):
    if request.method == 'GET':
        if request.user.userprofile.type == UserProfile.TYPE_STUDENT:
            userprofileform = forms.ChangeStudentInfoForm(instance=request.user.userprofile)
        else:
            userprofileform = forms.ChangeProfessorInfoForm(instance=request.user.userprofile)
        userform = forms.ChangeUserInfoForm(instance=request.user)
        return render(request, 'userinfo_change.html', {'userform': userform, 'userprofileform': userprofileform, })
    else:
        if request.user.userprofile.type == UserProfile.TYPE_STUDENT:
            userprofileform = forms.ChangeStudentInfoForm(request.POST, instance=request.user.userprofile)
        else:
            userprofileform = forms.ChangeProfessorInfoForm(request.POST, instance=request.user.userprofile)
        userform = forms.ChangeUserInfoForm(request.POST, instance=request.user)
        if userform.is_valid() and userprofileform.is_valid():
            userprofileform.save()
            userform.save()
            return render(request, 'userinfo_change.html',
                          {'userform': userform, 'userprofileform': userprofileform, 'success': True})
        else:
            return render(request, 'userinfo_change.html',
                          {'userform': userform, 'userprofileform': userprofileform, 'not_valid': True})


@login_required(login_url='/accounts/login/')
def user_info_view(request):
    user = request.user
    major = user.userprofile.MAJOR_CHOICES[user.userprofile.major][1]
    return render(request, "userinfo_view.html", {'user': user, 'major': major})


@login_required(login_url='/accounts/login/')
def my_project(request):
    username = request.user.userprofile.get_full_name()
    project_student_list = request.user.project_student_set.all()
    project_list = []
    for project in project_student_list:
        project_list.append(project.project)
    return render(request, "accounts_userprojectlist.html", {'username': username, 'project_list': project_list})


def get_changeable(request, project):
    changeable = False
    user = request.user
    project_student_list = project.project_student_set.all()
    for x in project_student_list:
        if x.student.id == user.id and x.is_superuser:
            changeable = True
    if project.status > 5:
        changeable = False
    return changeable


def get_judge(request, project_student_list):
    judge = False
    user = request.user
    for x in project_student_list:
        if x.student.id == user.id:
            judge = True
    return judge


@login_required(login_url='/accounts/login/')
def user_project_detail_view(request, project_id):
    project = Project.objects.get(id=project_id)
    project_student_list = project.project_student_set.all()
    judge = get_judge(request, project_student_list)
    if not judge:
        return HttpResponseRedirect('/accounts/info')
    changeable = get_changeable(request, project)
    return render(
        request,
        'accounts_userprojectdetails.html',
        {'project': project, 'student_list': project_student_list, 'changeable': changeable}
    )


@login_required(login_url='/accounts/login/')
def user_project_change_details(request, project_id):
    project = Project.objects.get(id=project_id)
    project_student_list = project.project_student_set.all()
    judge = get_judge(request, project_student_list)
    user = request.user
    if not judge or project.status >= 6:
        return HttpResponseRedirect('/accounts/info')

    attr = {'project_type': project.project_type,
            'project_name': project.name,
            'professor': project.professor.userprofile,
            'description': project.description,
            }
    len = project_student_list.__len__()
    if len > 1:
        tmp = 0
        i = 1
        while tmp < len:
            if project_student_list[tmp].student.id != user.id:
                attr.update({'partner' + str(i): project_student_list[tmp].student.username})
                i += 1
            tmp += 1
    if request.method == 'GET':
        form = forms.NewProjectForm(initial=attr)
        return render(
            request,
            'accounts_userprojectchangedetails.html',
            {'form': form, 'changeable': True}
        )
    else:
        form = forms.NewProjectForm(request.POST)
        if form.is_valid():
            project_type_id = request.POST.get('project_type', '')
            project_name = request.POST.get('project_name', '')
            professor_id = request.POST.get('professor', '')
            partner_list = []
            for x in range(1, 5):
                partner_list.append(request.POST.get('partner' + str(x), ''))
            description = request.POST.get('description', '')
            project_type = ProjectType.objects.get(id=project_type_id)
            professor = UserProfile.objects.get(id=professor_id).user
            for x in partner_list:
                if x != '' and User.objects.filter(username=x).__len__() == 0:
                    return render(request, 'new_project.html', {'form': form, 'wrong_student_id': True})
            project.name = project_name
            project.project_type = project_type
            project.description = description
            project.professor = professor
            project.save()
            project_student_list = project.project_student_set.all()
            for x in project_student_list:
                x.delete()
            Project_Student.objects.create(
                student=request.user,
                project=project,
                is_superuser=True,
            ).save()
            for x in partner_list:
                if x != '':
                    student = User.objects.get(username=x)
                    Project_Student.objects.create(
                        student=student,
                        project=project,
                        is_superuser=False,
                    ).save()
            return render(request, 'accounts_userprojectchangedetails.html',
                          {'form': form, 'success': True, 'changeable': True})
        return render(request, 'accounts_userprojectchangedetails.html',
                      {'form': form, 'not_valid': True, 'changeable': True})


@login_required(login_url='/accounts/login/')
def user_project_fund(request, project_id):
    project = Project.objects.get(id=project_id)
    project_student_list = project.project_student_set.all()
    judge = get_judge(request, project_student_list)
    if not judge:
        return HttpResponseRedirect('/accounts/info')
    changeable = get_changeable(request, project)
    if request.method == 'GET':
        form = forms.FundForm
        fund_list = project.fund_set.all()
        total = 0
        for x in fund_list:
            total += x.value
        return render(
            request,
            'accounts_userprojectfund.html',
            {'form': form, 'project': project, 'fund_list': fund_list, 'total': total, 'changeable': changeable}
        )
    else:
        form = forms.FundForm(request.POST)
        if form.is_valid():
            fund_type = request.POST.get('fund_type', '')
            value = request.POST.get('value', '')
            note = request.POST.get('note', '')
            if fund_type == '' or value == '' or int(value) < 0:
                return render(request, 'accounts_userprojectfund.html')
            Fund.objects.create(project=project, fund_type=fund_type, value=value, note=note).save()
            fund_list = project.fund_set.all()
            total = 0
            for x in fund_list:
                total += x.value
            return render(
                request,
                'accounts_userprojectfund.html',
                {'form': form, 'project': project, 'fund_list': fund_list, 'total': total, 'changeable': changeable}
            )
        else:
            return render(
                request,
                'accounts_userprojectfund.html',
                {'form': form, 'project': project, 'changeable': changeable, 'not_valid': True}
            )


@login_required(login_url='/accounts/login/')
def user_project_change_fund(request, project_id, fund_id):
    project = Project.objects.get(id=project_id)
    project_student_list = project.project_student_set.all()
    judge = get_judge(request, project_student_list)
    if project != Fund.objects.get(id=fund_id).project:
        judge = False
    if not judge:
        return HttpResponseRedirect('/accounts/info')
    changeable = get_changeable(request, project)
    if request.method == 'GET':
        fund = Fund.objects.get(id=fund_id)
        form = forms.FundForm(instance=fund)
        fund_list = project.fund_set.all()
        total = 0
        for x in fund_list:
            total += x.value
        return render(
            request,
            'accounts_userprojectchangefund.html',
            {'form': form, 'name': project.name, 'changeable': changeable}
        )
    else:
        form = forms.FundForm(request.POST)
        if form.is_valid():
            fund_type = request.POST.get('fund_type', '')
            value = request.POST.get('value', '')
            note = request.POST.get('note', '')
            if fund_type == '' or value == '' or int(value) < 0:
                return render(request, 'accounts_userprojectfund.html')
            fund = Fund.objects.get(id=fund_id)
            fund.fund_type = fund_type
            fund.value = value
            fund.note = note
            fund.save()
            return HttpResponseRedirect("../")
        else:
            return render(
                request,
                'accounts_userprojectchangefund.html',
                {'form': form, 'changeable': changeable, 'not_valid': True}
            )


@login_required(login_url='/accounts/login/')
def user_project_delete_fund(request, project_id, fund_id):
    project = Project.objects.get(id=project_id)
    project_student_list = project.project_student_set.all()
    judge = get_judge(request, project_student_list)
    fund = Fund.objects.get(id=fund_id)
    if project != fund.project:
        judge = False
    if not judge:
        return HttpResponseRedirect('/accounts/info')
    changeable = get_changeable(request, project)
    fund.delete()
    return HttpResponseRedirect('../../')


@login_required(login_url='/accounts/login/')
def new_credit(request):
    if UserProfile.TYPE_STUDENT != request.user.userprofile.type:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        form = forms.NewCreditForm()
        return render(request, 'new_credit.html', {'form': form})
    else:
        form = forms.NewCreditForm(request.POST, request.FILES)
        if form.is_valid():
            credit_name = request.POST.get("credit_name", "")
            get_project_date = format_date(str(request.POST.get("get_project_date")))
            credit_type = request.POST.get("credit_type")
            credit_second_type = request.POST.get("credit_second_type")
            credit_third_type = request.POST.get("credit_third_type")
            # credit_image = request.FILES['img']

            credit_now = Credit.objects.create(
                student=request.user,
                name=credit_name,
                get_project_date=get_project_date,
                credit_type=int(credit_type),
                credit_second_type=credit_second_type,
                credit_third_type=credit_third_type,
                # image = credit_image
            )
            credit_now.save()
            #credit_form =
            return render(request, 'new_credit.html',
                          {'form': form, 'success': "创建成功"})
        else:
            return render(request, 'new_credit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def edit_credit(request, id):
    if UserProfile.TYPE_STUDENT != request.user.userprofile.type:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'GET':
        credit = Credit.objects.get(id=int(id))
        form = forms.NewCreditForm({
            'credit_type': credit.credit_type,
            'credit_second_type': credit.credit_second_type,
            'credit_third_type': credit.credit_third_type,
            'get_project_date': credit.create_credit_date,
            'credit_name': credit.name,
            'credit_value': credit.value
        })
        return render(request, 'new_credit.html', {'form': form})
    else:
        form = forms.NewCreditForm(request.POST)
        if form.is_valid():
            credit = Credit.objects.get(id=int(id))
            credit.credit_type = int(request.POST.get("credit_type", 0))
            credit.credit_second_type = int(request.POST.get("credit_second_type", 11))
            credit.credit_third_type = int(request.POST.get("credit_third_type", 11))
            credit.name = request.POST.get("credit_name", "")
            credit.get_project_date = format_date(str(request.POST.get("get_project_date")))
            credit.save()
            return render(request, 'new_credit.html', {'form': form, 'success': "修改成功"})
        else:
            return render(request, 'new_credit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def user_credit_list_view(request):
    credit_list = request.user.credit_set.all()
    return render(request, 'credit.html', {'credit_list': credit_list})


@login_required(login_url='/accounts/login/')
def delete_credit(request, id):
    if UserProfile.TYPE_STUDENT != request.user.userprofile.type:
        return HttpResponseRedirect(reverse('home'))
    try:
        now_user = request.user
        now_credit = Credit.objects.get(id=int(id))
        if now_credit.student != now_user:
            return HttpResponseRedirect(reverse('home'))

        now_credit.delete()
        return HttpResponseRedirect(reverse('user_credit_list'))
    except:
        return HttpResponseRedirect(reverse('home'))


def format_date(date_str):
    try:
        date_list = time.strptime(str(date_str), '%Y-%m-%d')
    except:
        date_list = time.strptime(str(date_str), '%m/%d/%Y')
    year, month, day = date_list[0:3]
    return str(datetime.date(year, month, day))


#分页单页最多显示数量
PAGE_LIMIT = 3

@login_required(login_url='/accounts/login/')
def contact_student_list_view(request):
    student_list = UserProfile.objects.filter(type=UserProfile.TYPE_STUDENT)
    grade_list = student_list.values("grade").distinct()

    paginator = ExtendPaginator(student_list, PAGE_LIMIT)
    page_id = request.GET.get('page')
    try:
        student_list = paginator.page(page_id)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        student_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        student_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, "contact_student.html", {'student_list': student_list, 'grade_list': grade_list})


@login_required(login_url='/accounts/login/')
def contact_student_search_list_view(request):
    content = request.GET.get("search", "")
    grade = request.GET.get("grade", "ALL")
    student_list = UserProfile.objects.filter(type=UserProfile.TYPE_STUDENT)
    grade_list = student_list.values("grade").distinct()
    student_list = __search(grade, content, student_list)

    paginator = ExtendPaginator(student_list, PAGE_LIMIT)
    page_id = request.GET.get('page')
    try:
        student_list = paginator.page(page_id)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        student_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        student_list = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, "contact_student.html", {'student_list': student_list, 'grade_list': grade_list})


@login_required(login_url='/accounts/login/')
def contact_professor_list_view(request):
    professor_list = UserProfile.objects.filter(type=UserProfile.TYPE_PROFESSOR)
    paginator = ExtendPaginator(professor_list, PAGE_LIMIT)
    page_id = request.GET.get('page')
    try:
        professor_list = paginator.page(page_id)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        professor_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        professor_list = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, "contact_professor.html", {'professor_list': professor_list})

def contact_professor_search_list_view(request):
    content = request.GET.get("search", "")
    grade = "ALL"
    professor_list = UserProfile.objects.filter(type=UserProfile.TYPE_PROFESSOR)
    professor_list = __search(grade, content, professor_list)
    paginator = ExtendPaginator(professor_list, PAGE_LIMIT)
    page_id = request.GET.get('page')
    try:
        professor_list = paginator.page(page_id)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        professor_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        professor_list = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, "contact_professor.html", {'professor_list': professor_list})

@login_required(login_url='/accounts/login/')
def contact_professor(request):
    if request.method == 'GET':
        professor_list = UserProfile.objects.filter(type=UserProfile.TYPE_PROFESSOR)
        paginator = ExtendPaginator(professor_list, PAGE_LIMIT)
        page_id = request.GET.get('page')
        try:
            professor_list = paginator.page(page_id)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            professor_list = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            professor_list = paginator.page(paginator.num_pages)  # 取最后一页的记录
        return render(request, "contact_professor.html", {'professor_list': professor_list})
    else:
        content = request.POST.get("search", "")
        grade = "ALL"
        professor_list = UserProfile.objects.filter(type=UserProfile.TYPE_PROFESSOR)
        professor_list = __search(grade, content, professor_list)
        paginator = ExtendPaginator(professor_list, PAGE_LIMIT)
        page_id = request.GET.get('page')
        try:
            professor_list = paginator.page(page_id)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            professor_list = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            professor_list = paginator.page(paginator.num_pages)  # 取最后一页的记录
        return render(request, "contact_professor.html", {'professor_list': professor_list})


def __search(grade, content, user_list):
    if grade != "ALL":
        if grade == "None":
            user_list = user_list.filter(grade=None)
        else:
            user_list = user_list.filter(grade=int(grade))
    if content != "":
        temp_list = user_list
        user_list = []
        for temp in temp_list:
            if temp.user.username == content or temp.get_full_name() == content or temp.user.first_name + temp.user.last_name == content:
                user_list.append(temp)
    print(user_list)
    return user_list
