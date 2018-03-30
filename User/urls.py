#coding:utf-8
from django.conf.urls import url
from views import *
urlpatterns = [
    url(r"^phone_valid/$",phone_valid),
    url(r"^register/$", register)
]
