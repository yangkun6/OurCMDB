#coding:utf-8
from django.shortcuts import render
from User.models import CMDBUser
import hashlib
from django.http import HttpResponseRedirect

#加密函数
def getmd5(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

#校验电话重复
def valid_phone(phone):
    try:
        user = CMDBUser.objects.get(phone=phone)  # 尝试在数据库查询改手机号
    except:
        return phone  # 假如不存在，就返回手机号，可以注册
    else:
        return "手机号重复"


#cookie校验装饰器
def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        c_username = cookie.get("username")
        s_username = request.session.get("username")
        is_login = request.session.get("isLogin")
        if c_username and s_username and c_username == s_username and is_login:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login")
    return inner