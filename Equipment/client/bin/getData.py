#!/usr/bin/python
#coding:utf-8
import os
import uuid
import psutil
"""
采集静态脚本
hostname
mac
ip
system
sys_version
cpu_conunt
memory
disk
"""

class GetData:
    def __init__(self):
        self.result = {}
        self.sys = os.name#系统区分
	if self.sys == "nt":
           self.system = "windows" 
           self.hostname = os.getenv("computername")#获取win主机名
        elif self.sys == "posix":
           self.system = "Linux"
	   self.hostname = os.popen("hostname").read()#获取linux主机名
        else:
           self.system = "Unix"
           self.hostname = "unkwon"
    def get_hostname(self):
        return self.hostname
    def get_system(self):
        return self.system
    def get_mac(self):#获mac固定
        mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
        result = ":".join([mac[e:e+2] for e in range(0,11,2)])
	return result
    def get_version(self):#获版本
        version = os.popen("cat /etc/issue").read()
        return version
    def get_cpu_count(self):#获cpu个数
        count = psutil.cpu_count()
        return str(count)
    def get_memory(self):#获内存
        memory = psutil.virtual_memory().total
        return str(memory)
    def get_disk(self):#获硬盘
        disk = psutil.disk_usage("/").total
        return str(disk)
    def getData(self):#总数据整理
        data_method = GetData.__dict__
        for key,value in data_method.items():
	    if "get_" in key and callable(value):
                name = key.replace("get_","")
                self.result[name] = value(self).replace("\n","").replace("\r","").replace("\\","")
        return self.result
if __name__ == "__main__":
    data = GetData()
    result = data.getData()
    print(result)


