#coding:utf-8
import random
result_list = []#测试的数据
for i in range(50):
    hostname = "local_%s"%i
    mac = "00:0c:2%s:cd:%sb:e%s"%(random.randint(1,9),random.randint(1,9),random.randint(1,9))
    ip = "192.168.1.%s"%i
    sys_type = random.choice(["Windows","Linux","Mac"])
    if sys_type == "Windows":
        versionList = ["win95","win98","win2000","win xp","win7","win8","win10"]
    elif sys_type == "Linux":
        versionList = ["Linux ", "Ubuntu", "OpenSUSE", "Fedora", "RHEL", "CentOS "]
    else:
        versionList = ["OS X Mountain Lion","OS X Mavericks","OS X Yosemite","OS X El Capitan","macOS Sierra",]
    sys_version = random.choice(versionList)
    cpu_count = random.randint(1,4)
    disk = random.choice(["SEAGATE 200GB SAS 10K 2.5",
                          "SEAGATE 400GB SAS 10K 2.5",
                          "SEAGATE 600GB SAS 10K 2.5"])
    memory = random.choice(["SAMSUNG DDR4 2400T DDR3 4G",
                            "SAMSUNG DDR4 2400T DDR3 8G",
                            "SAMSUNG DDR4 2400T DDR3 16G",
                            "SAMSUNG DDR4 2400T DDR3 32G"])
    result =  {
         "hostname": hostname,
         "mac": mac,
         "ip": ip,
         "sys_type": sys_type,
         "sys_version": sys_version,
         "cpu_count": cpu_count,
         "disk": disk,
         "memory": memory
         }
    result_list.append(result)

print(result_list)