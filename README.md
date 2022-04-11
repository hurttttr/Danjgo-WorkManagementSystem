## 环境要求

Django 3.1.5

Django-apscheduler  0.5.2

安装

```python
pip install Django django-apscheduler
```

## 使用方式

填写config文件中的相关信息包括，mysql数据库的相关信息，qq邮箱的账号和授权码

```
python manage.py runserver 8000 # 启动服务器

#同步数据库(第一次使用)
python manage.py makemigrations
python manage.py migrate
#创建管理员(第一次使用)
python manage.py createsuperuser#然后根据提示输出用户名，电子邮件，密码
```

## 注意事项

由于Django-apscheduler的版本更新，我在开发时修改了其源代码以实现定时任务功能，若想实现此功能可以尝试以下解决方法或者注释此模块运行

### 添加定时任务后再次启动提示Job identifier (test) conflicts with an existing job

原因：django-apscheduler的表存储方式发生了改变，现在没有name项，使用id作为name

解决方法：

①  每次启动或者修改后清空`django_apscheduler_djangojob`和`django_apscheduler_djangojobexecution`这两张表

②  打开python文件下`lib\site-packages\django_apscheduler\jobstores.py`文件（具体路径随每个环境可能有所不同）修改add_job函数为

```python
def add_job(self, job: AppSchedulerJob):
    with transaction.atomic():
        try:
            obj = DjangoJob.objects.filter(id=job.id)
                if obj:
                    DjangoJobStore.update_job(self,job)
                else:
                    return DjangoJob.objects.create(
                        id=job.id,                        next_run_time=get_django_internal_datetime(job.next_run_time),
                        job_state=pickle.dumps(job.__getstate__(), self.pickle_protocol),
                    )
                except IntegrityError:
                    raise ConflictingIdError(job.id)

```

