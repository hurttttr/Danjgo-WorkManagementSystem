from django.urls import path
from app import views

urlpatterns = [
    path('login/', views.login),  # 登录
    path('', views.login),  # 登录
    path('logout/', views.logout),  # 注销
    path('register/', views.register),  # 注册
    path('index/', views.index),  # 首页
    path('add_work/', views.add_work),  # 添加作业
    path('add_user/', views.add_user),  # 添加用户
    path('add_userlist/', views.add_userlist),  # 批量导入用户
    path('upload_work/', views.upload_work),  # 提交作业
    path('list_work/', views.list_work),  # 用户作业列表
    path('list_work_admin/', views.list_work_admin),  # 管理员作业列表
    path('list_user/', views.list_user),  # 用户列表
    path('detail/', views.detail),  # 个人信息
    path('edit/', views.edit),  # 编辑作业
    path('edit_user/', views.edit_user),  # 编辑用户
    path('delete/', views.delete),  # 删除作业
    path('delete_user/', views.delete_user),  # 删除用户
    path('download/', views.download),  # 下载作业
    path('download_template/', views.download_template),  # 下载模板
    path('download_template1/', views.download_template1),  # 下载导入的用户模板
]
