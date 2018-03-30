#coding:utf-8
from django.conf.urls import url
from views import *
urlpatterns = [
    url(r"^$", eqList),
    url(r"^eqList/$",eqList),
    url(r"^eqDatas/(\d+)$", eqDatas),
    url(r"^equip_api/", equip_api),
    url(r"^gateone/$", gateone),
    url(r"^addEquipment/$", addEquipment),
    url(r"^Terminal/(\d{1,3})/$", Terminal),
    url(r"^get_auth_obj/$", get_auth_obj)
]