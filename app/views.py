import requests
from datetime import datetime
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from app import models
from app import function


def test(request):
    return HttpResponse("") # 返回字符串
    return render(request, "") # 返回一个网页
    return redirect('') # 重定向

# Create your views here.
#登录
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if not user_obj:
            return render(request, "login.html", {'error': '用户名或者密码错误'})
        else:
            auth.login(request, user_obj)
            rep = redirect('/app/index')
            if user_obj.is_superuser:
                # rep = redirect('/app/list_work_admin')
                rep.set_cookie("is_superuser", True)
            else:
                # rep = redirect('/app/list_work')
                rep.set_cookie("is_superuser", False)
            rep.set_cookie("username", username, max_age=60 * 60 * 24 * 14) #设置cookie保存14天
            return rep
    else:
        return render(request, "login.html")


@login_required

def logout(request):
    auth.logout(request)
    rep = redirect("/app/login")
    rep.delete_cookie("username")
    rep.delete_cookie("is_superuser")
    return rep


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)  # get能且仅能返回一条数据。
            return render(request, "register.html", {'error': '该用户已经存在'})
        except User.DoesNotExist:
            User.objects.create_user(username=username, password=password, first_name=firstname)
            return redirect("/app/login/")  # 重定向至登录界面
            pass
    else:
        username = request.COOKIES.get('username')
        return render(request, "register.html", {'username': username})


@login_required
# 初始界面
def index(request):
    username = request.COOKIES.get('username')
    is_superuser = request.COOKIES.get("is_superuser")
    if username == 'root':
        flag = True
    else:
        flag = False
    return render(request, "index.html", {'username': username, 'is_superuser': is_superuser, 'flag': flag})


@login_required
# 添加作业(管理员)
def add_work(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    if request.method == 'POST':
        workname = request.POST.get('workname')
        deadline = request.POST.get('deadline')
        deadlinetime = request.POST.get('deadlinetime')
        email = request.POST.get('email')
        deadline = ' '.join([deadline, deadlinetime])
        t = models.Work.objects.create(name=workname, deadline=deadline, email=email)
        function.createDirectory('upload/' + str(t.id))
        return redirect("/app/list_work_admin")  # 重定向至作业列表
    else:
        username = request.COOKIES.get('username')
        return render(request, "add_work.html", {'username': username, 'is_superuser': is_superuser})


@login_required
def add_userlist(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    username = request.COOKIES.get("username")
    if username != 'root':
        return redirect('/app/index')
    if request.method == 'POST':
        path = 'upload/cache/名单.xlsx'
        obj = request.FILES.get('file')
        function.saveUploadedFile(obj, path)
        function.addUsers()
        return render(request, 'add_userlist.html', {'username': username, 'is_superuser': is_superuser, 'success': True})
    else:
        return render(request, 'add_userlist.html', {'username': username, 'is_superuser': is_superuser})


@login_required
# 上传作业
def upload_work(request):
    username = request.COOKIES.get('username')
    is_superuser = request.COOKIES.get("is_superuser")
    student = User.objects.get(username=username)
    id = request.GET.get("id")
    if request.method == 'GET':
        return render(request, "upload_work.html", {'id': id, 'username': username, 'is_superuser': is_superuser})
    else:
        path = 'upload/{}/{}'.format(id, student.username + '+' + student.first_name)
        upload, _ = models.Upload.objects.get_or_create(username=username, work_id=id)
        upload.time = datetime.now()
        upload.save()
        obj = request.FILES.get('file')
        path += '.' + obj.name.split('.')[1]
        function.saveUploadedFile(obj, path)
        return render(request, "upload_work.html",
                      {'id': id, 'username': username, 'is_superuser': is_superuser, 'success': True})


@login_required
# 用户作业列表
def list_work(request):
    work_list = models.Work.objects.all()
    is_superuser = request.COOKIES.get("is_superuser")
    username = request.COOKIES.get('username')
    work = models.Upload.objects.filter(username=username)
    finish = []
    for i in work:
        finish.append(i.work_id)
    return render(request, "list_work.html",
                  {'work_list': work_list, 'username': username, 'is_superuser': is_superuser, 'finish': finish})


@login_required
# 管理员作业列表
def list_work_admin(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    work_list = models.Work.objects.all()
    username = request.COOKIES.get("username")
    work = models.Upload.objects.filter(username=username)
    finish = []
    for i in work:
        finish.append(i.work_id)
    return render(request, "list_work_admin.html",
                  {'work_list': work_list, 'username': username, 'is_superuser': is_superuser, 'finish': finish})


@login_required
# 个人信息
def detail(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        username = request.GET.get("username")
        _t = User.objects.get(username=username)
        _t.first_name = first_name
        if password:
            _t.set_password(password)
        _t.save()
        return render(request, "detail.html", {'student': _t, 'username': username, 'is_superuser': is_superuser})
    else:
        username = request.COOKIES.get("username")
        student = User.objects.get(username=username)
        return render(request, "detail.html", {'student': student, 'username': username, 'is_superuser': is_superuser})


@login_required
# 作业编辑(管理员)
def edit(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    if request.method == "GET":
        id = request.GET.get("id")
        work = models.Work.objects.get(id=id)
        username = request.COOKIES.get('username')
        return render(request, "edit.html", {'work': work, 'username': username, 'is_superuser': is_superuser})
    else:
        id = request.GET.get("id")
        workname = request.POST.get('workname')
        deadline = request.POST.get('deadline')
        deadlinetime = request.POST.get('deadlinetime')
        email = request.POST.get('email')
        _t = models.Work.objects.get(id=id)
        _t.name = workname
        _t.deadline = deadline + ' ' + deadlinetime
        _t.email = email
        _t.save()
        return redirect('/app/list_work_admin/')


@login_required
# 作业删除(管理员)
def delete(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    id = request.GET.get("id")
    models.Work.objects.get(id=id).delete()
    # 删除文件夹
    function.deleteDirectory('upload/' + str(id))
    # 删除与作业有关的记录
    models.Upload.objects.filter(work_id=id).delete()
    return redirect('/app/list_work_admin/')


@login_required
def download(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    username = request.COOKIES.get('username')
    if request.method == 'POST':
        id = request.GET.get('id')
        work = models.Work.objects.get(id=id)
        obj = request.FILES.get('file')
        if obj is None:
            path = 'upload/cache/名单.xlsx'
        else:
            path = 'upload/cache/' + str(id)
            path += '.' + obj.name.split('.')[1]
            function.saveUploadedFile(obj, path)  # 保存名单
        print(id)
        function.writeRecord(path, id)  # 写入完成情况
        function.zipDirectory(id)
        new_path = 'upload/{}.zip'.format(id)
        file = open(new_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}.zip"'.format(work.name)  # 不支持中文文件名
        return response
    else:
        id = request.GET.get('id')
        return render(request, "download.html", {'id': id, 'username': username, 'is_superuser': is_superuser})


@login_required
# 下载名单模板
def download_template(request):
    file = open('static/files/模板.xlsx', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="template.xlsx"'  # 不支持中文文件名
    return response


@login_required
# 下载导入名单模板
def download_template1(request):
    file = open('static/files/导入模板.xlsx', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="template.xlsx"'  # 不支持中文文件名
    return response


@login_required
def list_user(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    username = request.COOKIES.get('username')
    if username != 'root':
        return redirect('/app/index')
    if request.method == "POST":
        pass
    else:
        user_list = User.objects.all()
        return render(request, 'list_user.html',
                      {'user_list': user_list, 'username': username, 'is_superuser': is_superuser})


@login_required
def edit_user(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    username = request.COOKIES.get('username')
    if username != 'root':
        return redirect('/app/index')
    id = request.GET.get("id")
    user = User.objects.get(id=id)
    if request.method == "POST":
        superuser = request.POST.get("superuser")
        name = request.POST.get("first_name")
        password = request.POST.get("password")
        user.first_name = name
        user.is_superuser = superuser
        if password:
            user.set_password(password)
        user.save()
        return render(request, 'edit_user.html',
                      {'user': user, 'username': username, 'is_superuser': is_superuser, 'success': True})
    else:
        return render(request, 'edit_user.html',
                      {'user': user, 'username': username, 'is_superuser': is_superuser})


@login_required
def delete_user(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    username = request.COOKIES.get('username')
    if username != 'root':
        return redirect('/app/index')
    id = request.GET.get("id")
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/app/list_user")


@login_required
def add_user(request):
    is_superuser = request.COOKIES.get("is_superuser")
    if is_superuser == 'False':
        return redirect('/app/list_work')
    username = request.COOKIES.get('username')
    if username != 'root':
        return redirect('/app/index')
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("first_name")
        password = request.POST.get("password")
        superuser = request.POST.get("superuser")
        if superuser:
            User.objects.create_user(username=username, password=password,first_name=name)
        else:
            User.objects.create(username=name, password=password,first_name=name)
        return redirect('/app/list_user')
    else:
        return render(request, 'add_user.html',
                      {'username': username, 'is_superuser': is_superuser})


#定时任务
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')

# 每天分钟执行这个任务
@register_job(scheduler, 'interval', id='test',seconds=60)
def test():
    # 具体要执行的代码
    function.checkDeadline()

# 注册定时任务并开始
register_events(scheduler)
scheduler.start()