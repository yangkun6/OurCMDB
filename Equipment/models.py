#coding:utf-8
from django.db import models

class Equipment(models.Model):#设备表
    hostname = models.CharField(max_length = 32,verbose_name = "主机名")
    mac = models.CharField(max_length = 32,verbose_name = "mac地址")
    ip = models.CharField(max_length = 32,verbose_name = "ip地址")
    sys_type = models.CharField(max_length = 32,verbose_name = "系统类型")
    sys_version = models.CharField(max_length = 32,verbose_name = "系统版本")
    cpu_count = models.IntegerField(verbose_name = "cpu个数")
    disk = models.CharField(max_length = 32,verbose_name = "硬盘")
    memory = models.CharField(max_length = 32, verbose_name = "内存")

    def __unicode__(self):#后台展示和查询
        return "%s:%s"%(self.hostname,self.ip)#传输多个值

class ApiToken(models.Model):#token表
    value = models.CharField(max_length = 32,verbose_name = "值")
    types = models.CharField(max_length = 32,verbose_name = "token类型")
    time = models.DateTimeField(verbose_name = "注册时间")


# Create your models here.
