#coding:utf-8
import os
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from models import Equipment
from User.forms import Register
import paramiko

import time,hmac,hashlib,json


def eqList(request):#服务器展示页
    register = Register()
    return render(request,"eqList.html",locals())

#第一步获取链接
def getConnection(ip,username,password,fun):
    """
    :param ip:
    :param username:
    :param password:
     链接服务器，生成实例
    """
    result = {"state": "error", "data": ""}
    try:
        transport = paramiko.Transport((ip,22))#通过paramiko
        transport.connect(username = username,password = password)
    except Exception as e:
        result["data"] = str(e)
    else:
        fun(transport,ip,username,password)
        result["state"] = "success"
        result["data"] = transport
    return result

#第二步源文件下传
def putFile(transport,ip,username,password):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR,"Equipment/client/bin")
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.put(os.path.join(file_path,"main.py"),"/opt/CMDB/main.py")
        sftp.put(os.path.join(file_path,"getData.py"), "/opt/CMDB/getData.py")
        sftp.put(os.path.join(file_path,"sendData.py"), "/opt/CMDB/sendData.py")
    except Exception as e:
        print(e)
    finally:
        transport.close()
#第三步整合执行命令
def doCommand(transport,ip,username,password):
    #定义命令
    createCommand = "mkdir /opt/CMDB/"
    testCommand = "ls /opt"
    execCommand = "python /opt/CMDB/main.py"
    #进行ssh链接
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    #创建目录
    try:
        ssh.exec_command(createCommand)
        while True:
            stdin,stdout,stderr = ssh.exec_command(testCommand)
            if "CMDB" in stdout.read():
                getConnection(ip,username,password,putFile)
                ssh.exec_command(execCommand)
                break
    except Exception as e:
        print(e)
    finally:
        transport.close()
#第四步数据的调用
def addEquipment(request):
    result = {"state":"error","data":""}
    if request.method == "POST":
        requestData = request.POST
        ip = requestData.get("ipaddress","")
        username = requestData.get("username","")
        password = requestData.get("password","")
        if ip and username and password:
            #调用方法执行上传
            getConnection(ip,username,password,doCommand)
            result["state"] = "success"
            result["data"] = "success"
        else:
            result["data"] = "ip and username and password not be null"
    else:
        result["data"] = "your request must be post"

    return JsonResponse(result)
#获取总数据并分页展示
def eqDatas(request,pagenum):
    pagenum = int(pagenum)
    start = (pagenum-1)*10
    end = pagenum*10


    all_data = Equipment.objects.all()[start:end]#数据库统计数据总数
    result_list = []
    eq_len = len(Equipment.objects.all())#查数据库的总数据
    for data in all_data:#生成数据如下
        dicts = {
            'disk': data.disk,
            'sys_version': data.sys_version,
            'mac': data.mac,
            'cpu_count': data.cpu_count,
            'memory': data.memory,
            'ip': data.ip,
            'hostname': data.hostname,
            'sys_type': data.sys_type,
            'id': data.id
        }
        result_list.append(dicts)

    if eq_len%10:
        Prange = range(1,eq_len/10+2)
    else:
        Prange = range(1,eq_len/10+1)
    Prange.reverse()
    result = {"result":result_list,"Prange":Prange}
    return JsonResponse(result)

@csrf_exempt#csrf安全的装饰器
def equip_api(request):#下面客户传来的数据接收并存库
    result = {"statue":"error","data":""}
    if request.method == "POST":
        requestData = request.POST
        hostname = requestData.get("hostname")
        mac = requestData.get("mac")
        ip = request.META["REMOTE_ADDR"]
        system_type = requestData.get("version")
        memory = requestData.get("memory")
        disk = requestData.get("disk")
        cpu_count = requestData.get("cpu_count")
        system_version = requestData.get("system")
        try:
            eq = Equipment()
            eq.hostname = hostname
            eq.mac = mac
            eq.ip = ip
            eq.sys_type = system_type
            eq.memory = memory
            eq.disk = disk
            eq.cpu_count = cpu_count
            eq.sys_version = system_version
            eq.save()
        except Exception as e:
            result["data"] = str(e)
        else:
            result["statue"] = "success"
            result["data"] = "your data is saved"
    else:
        result["data"] = "request must be post"
    return JsonResponse(result)

def gateone(request):#测试页面
    return render(request,"cmdb_terminal.html")


def Terminal(request,id):#<a>链接</a>不同的客户页面去
    id = int(id)
    equipment = Equipment.objects.get(id = id)
    ip = equipment.ip
    port = 22
    username = "root"
    return render(request,"Terminal.html",locals())

def create_signature(secret,*parts):#gateone加密
    hash = hmac.new(secret,digestmod = hashlib.sha1)
    for parts in parts:
        hash.update(str(parts))
    return hash.hexdigest()

def get_auth_obj(request):#gateone配置部分
    user = request.user.username
    gateone_server = "https://192.168.1.9:443"

    secret = "M2I5ODM4MzhlNGJiNGNlNGIzMzE3NjY1MWQwNDIyMTU0Z"
    api_key = "ZDM5ZjYwYjljMmU0NGZkNDk2NzVmZTVmMzI2NzYxNWEwZ"

    authobj = {
        'api_key': api_key,
        'upn': "gateone",
        'timestamp': str(int(time.time() * 1000)),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    my_hash = hmac.new(secret, digestmod=hashlib.sha1)
    my_hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])

    authobj['signature'] = my_hash.hexdigest()
    auth_info_and_server = {"url": gateone_server, "auth": authobj}
    valid_json_auth_info = json.dumps(auth_info_and_server)
    return HttpResponse(valid_json_auth_info)






# Create your views here.
