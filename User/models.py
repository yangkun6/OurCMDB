#coding:utf-8
from django.db import models

class CMDBUser(models.Model):#用户表
    username = models.CharField(max_length = 32,verbose_name = "用户名")
    password = models.CharField(max_length = 32, verbose_name = "密码")
    email = models.EmailField(verbose_name = "邮箱")
    phone = models.CharField(max_length = 32,verbose_name = "电话")
    photo = models.ImageField(upload_to = "images",verbose_name = "照片")
    #ImageField必须在安装pil或者pillow的基础上使用
    def __unicode__(self):
        return self.username

class Permission(models.Model):#权限表
    name = models.CharField(max_length = 32,verbose_name = "权限名称")
    obj_id = models.IntegerField(verbose_name = "操作对象")
    description = models.TextField(verbose_name = "权限描述")

    def __unicode__(self):
        return self.name

class Group(models.Model):#组表
    name = models.CharField(max_length = 32,verbose_name = "组名称")

    def __unicode__(self):
        return self.name

class User_group(models.Model):#用户和组
    user_id = models.IntegerField(verbose_name = "用户id")
    group_id = models.IntegerField(verbose_name = "组id")

class User_permission(models.Model):#用户和权限
    user_id = models.IntegerField(verbose_name = "用户id")
    permission_id = models.IntegerField(verbose_name = "权限id")

class Permission_group(models.Model):#权限和组
    permission_id = models.IntegerField(verbose_name = "权限id")
    group_id = models.IntegerField(verbose_name = "组id")










# Create your models here.
