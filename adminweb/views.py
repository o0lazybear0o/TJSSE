from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from accounts.models import UserProfile
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
        return render(request, 'adminweb_newstudent.html', {'form': form,})
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
            for x in range(id1, id2+1):
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
        return render(request, 'adminweb_newprofessor.html', {'form': form,})
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
