#!/usr/bin/python
#coding:utf-8
import urllib
import urllib2 

class Sender:
    """
      默认接口不接受cookie
    """
    def __init__(self,url,data):
        self.url = url
        self.data = urllib.urlencode(data)
    def get_request(self,header = {}):#数据请求
        self.request = urllib2.Request(self.url,data = self.data,headers = header)
    def get_response(self):#数据发送
        self.response = urllib2.urlopen(self.request)
        result = self.response.read()
    	return result

