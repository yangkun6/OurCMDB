#coding:utf-8
from django.shortcuts import render_to_response,render
from django.http import JsonResponse,HttpResponseRedirect
from OurCMDB.views import valid_phone,getmd5,loginValid
from forms import Register
from models import CMDBUser
from PIL import Image

def login(request):#登陆效验
    if request.method == "POST":
        #如果是post请求根据name进行数据获取
        phone = request.POST["phone"]
        password = request.POST["password"]
        #尝试获取数据库里提交的手机号的信息
        try:
            user = CMDBUser.objects.get(phone = phone)
        except: #如果获取失败,返回登录页
            return HttpResponseRedirect("/login")
        else:
            md5_password = getmd5(password) #对提交的密码进行加密
            if user.password == md5_password: #比对密码
                response = HttpResponseRedirect("/index") #实例化响应
                response.set_cookie("username",user.username) #设置cookie
                request.session["username"] = user.username #设置session
                request.session["isLogin"] = True #设置session
                token = request.COOKIES.get("token")
                if token:
                    return response
                else:
                    return HttpResponseRedirect("/login")
            else:
                return HttpResponseRedirect("/login")
    response = render(request,"login.html")
    response.set_cookie("token","hello")
    return response

@loginValid#进主页前cookie的效验装饰器
def index(request):
    register = Register()
    return render(request,"index.html",locals())#render_to_response("index.html",locals())

def phone_valid(request):#手机号效验
    res = {"type":"error","data":""}
    if request.method == "GET":
        phone = request.GET["phone"]
        result = valid_phone(phone)
        if phone == result:
            res["type"] = "success"
        else:
            res["data"] = result
    else:
        res["data"] = "request must be get"
    return JsonResponse(res)

def register(request):#注册页面的效验和存库
    res = {"type": "error", "data": ""}
    if request.method == "POST":
        reg = Register(request.POST,request.FILES) #对数据进行校验
        #reg = Register({"username":"while","password“:”123456“})
        if reg.is_valid():
            cleand_data = reg.cleaned_data #验证通过的字典形式的数据
            username = cleand_data["username"]
            password = cleand_data["password"]
            email = cleand_data["email"]
            phone = cleand_data["phone"]
            photo = cleand_data["photo"]

            user = CMDBUser()
            user.username = username
            user.password = getmd5(password) #加密密码
            user.email = email
            user.phone = phone

            #保存图片
            name = "static/image/"+photo.name
            img = Image.open(photo)
            img.save(name)
            #数据库当中存储图片的路径
            user.photo = "image/"+photo.name
            user.save()

            res["type"] = "success"
            res["data"] = "success"
        else:
            res["data"] = reg.errors
    else:
        res["data"] = "request error"
    return JsonResponse(res)
def exit(request):#登出
    response = HttpResponseRedirect("/login")
    response.set_cookie("token", "hello")  # 退出设置
    request.session["isLogin"] = False
    return response
def user(request):#用户中心
    register = Register()
    user1 = CMDBUser.objects.all()
    return render(request, "user.html", locals())
# Create your views here.
