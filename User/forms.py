#coding:utf-8
import re
from django import  forms
from django.forms import ValidationError
from models import CMDBUser
from OurCMDB.views import valid_phone

class Register(forms.Form):#注册表单加验证
    username = forms.CharField(
        max_length = 32,
        min_length = 6,
        label = "用户名",
        widget = forms.TextInput(attrs = {"class":"form-control","placeholder":"用户名"})
    )
    password = forms.CharField(
        max_length = 32,
        min_length = 6,
        label = "密码",
        widget = forms.PasswordInput(attrs = {"class":"form-control","placeholder":"密码"})
    )
    email = forms.CharField(
        max_length = 32,
        min_length = 6,
        label = "邮箱",
        widget = forms.TextInput(attrs = {"class":"form-control","placeholder":"邮箱"})
    )
    phone = forms.CharField(
        max_length = 32,
        min_length = 11,
        label = "电话",
        widget = forms.TextInput(attrs = {"class":"form-control","placeholder":"电话"})
    )
    photo = forms.ImageField(label = "用户头像")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone") #获取提交的电话的值
        result = valid_phone(phone)
        if result == phone:
            return phone
        else:
            raise ValidationError(result)


    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password.isdigit():
            raise ValidationError("密码不可以完全以数字组成")
        elif password.isalpha():
            raise ValidationError("密码不可以完全以字母组成")
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        res = re.match(r"\w+@\w+\.[a-zA-Z]+",email)
        if res:
            return email
        else:
            raise ValidationError("邮箱格式错误")







