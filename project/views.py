from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, render_to_response
from TJSSE.utils import ExtendPaginator
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import Project,Project_Student
from .forms import SearchForm
from django.db.models import Q
# Create your views here.

PAGE_LIMIT = 10

@login_required(login_url='/accounts/login/')
def project_list_view(request):
    proj_list=Project.objects.all() #获取所有的项目
    search_form=SearchForm()

    paginator = ExtendPaginator(proj_list, PAGE_LIMIT)
    page_id = request.GET.get('page')
    try:
        proj_list = paginator.page(page_id)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        proj_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        proj_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'project/project_list.html', {'project_list':proj_list,\
                                                         'form':search_form,\
                                                         'search_choice':Project.STATUS_CHOICES})
# @login_required(login_url='/accounts/login/')
# def project_search_list_view(request):
#     search_val=request.GET['search_val']
#     proj_type=int(request.GET['project_type'])
#     status_type=int(request.GET['status_type'])
#     search_date=request.GET['search_date']
#

@login_required(login_url='/accounts/login/')
def project_search_list_view(request):
    search_infor=getSearchInfor(request)
    if search_infor == None:  #通过urls直接访问project/search
        return project_list_view(request)
    else:
        #根据关键字可能分别为指导老师编号/学生编号/项目名称/项目截止时间
        proj_list=Project.objects
        if search_infor['search_val']!='':
            proj_list=proj_list.filter(Q(professor__username=search_infor['search_val'])|\
                                             Q(project_student__student__username=search_infor['search_val'])|\
                                             Q(name__contains=search_infor['search_val']))
        #根据项目类型以及状态以及截止时间的查询
        if search_infor['proj_type']!=SearchForm.DEFAULT_VAL:
            proj_list=proj_list.filter(project_type__type=search_infor['proj_type'])
        if search_infor['status_type']!=SearchForm.DEFAULT_VAL:
            proj_list=proj_list.filter(status=search_infor['status_type'])
        if search_infor['search_date']!='':
            proj_list=proj_list.filter(endtime__gte = search_infor['search_date'])

        #删除重复
        proj_list=proj_list.distinct()
        search_form=SearchForm()

        paginator = ExtendPaginator(proj_list, PAGE_LIMIT)
        page_id = request.GET.get('page')
        try:
            proj_list = paginator.page(page_id)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            proj_list = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            proj_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

        return render(request, 'project/project_list.html', {'project_list':proj_list,\
                                                             'form':search_form,\
                                                             'search_choice':Project.STATUS_CHOICES})


@login_required(login_url='/accounts/login/')
def project_detail_view(request, project_id):
    search_form=SearchForm()

    project = Project.objects.get(pk = project_id)
    proj_stu_list=Project_Student.objects.filter(project=project)
    stu_list=[proj_stu.student.get_full_name() for proj_stu in proj_stu_list]

    return render(request, 'project/project_detail.html', {'project':project,\
                                                           'search_choice':Project.STATUS_CHOICES,\
                                                           'stu_list':stu_list,\
                                                           'form':search_form})

def getSearchInfor(request):
    search_form=SearchForm(request.POST)
    if search_form.is_valid():
        search_val=request.POST['search_val']
        proj_type=int(request.POST['project_type'])
        status_type=int(request.POST['status_type'])
        search_date=request.POST.get('search_date','')
        return {'search_val':search_val,'proj_type':proj_type,'status_type':status_type,'search_date':search_date}
    else:
        return None