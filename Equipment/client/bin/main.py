#!/usr/bin/python
#coding:utf-8
from getData import GetData
from sendData import Sender
import datetime

url = "http://192.168.1.5:8000/eq/equip_api/"#服务器的ip及提交的函数
try:
    data = GetData()
    sendData = data.getData()

    sender = Sender(url,sendData)#向指定的url发送获取的数据
    sender.get_request()
    response = sender.get_response()
    print(response)
except Exception as e:#报错机制
    with open("/opt/CMDB/log.txt","a+") as f:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = "[%s]:%s\n"%(time,str(e))
        f.write(content)

