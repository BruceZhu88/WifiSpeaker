#coding=utf-8
#
# Author: Bruce Zhu
#

import subprocess
import ctypes
import os
import sys
import time
import re
from src.common.logger_config import logger

class windowsWifi():
    def __init__(self, framelogPrint):
        self.framelogPrint = framelogPrint
        #*************************************************************
        # Chinese: 0x804
        # English: 0x409
        dll_handle = ctypes.windll.kernel32
        id = hex(dll_handle.GetSystemDefaultUILanguage())
        if id=="0x804":
            system_language = "Chinese"
        elif id=="0x409":
            system_language = "English"
        else:
            system_language = ""
        #*************************************************************
        if system_language=="Chinese":
            self.wifiState = "已连接"
            self.wifiStateFind = "状态"
            self.ipType = "动态"
        elif system_language=="English":
            self.wifiState = "connected"
            self.wifiStateFind = "State"
            self.ipType = "dynamic"

    def printLog(self, info):
        try:
            self.framelogPrint.addLog(info, ' ')
        except Exception as e:
            logger.debug("Error when printLog: {}".format(e))
            sys.exit()

    def connect_wifi(self, name):
        self.printLog("Try to connect wifi --> %s"%name)
        p = os.popen("netsh wlan connect name=\"{name}\"".format(name=name))
        content = p.read()
        self.printLog(content)
        #os.system("netsh wlan connect name=%s" % name)

    def wifi_status(self):
        self.printLog("Checking wifi status...")
        p = os.popen("netsh wlan show interfaces")
        content = p.read()
        return content

    def check_wifi(self, wifiName):
        #self.printLog(content)
        for i in range(0,5):
            content = self.wifi_status()
            try:
                wifiSSID = re.findall(u"SSID(.*)",content)[0].split(": ")[1]
                wifiState = re.findall(u"%s(.*)"%self.wifiStateFind,content)[0].split(": ")[1]
                #self.printLog(wifiState)
                if wifiSSID == wifiName:
                    if wifiState == self.wifiState:
                        self.printLog("Wifi %s connected!"%wifiName)
                        return True
                self.printLog("Wifi [%s] did not connected!"%wifiName)
            except Exception as e:
                logger.error("Check wifi:{}".format(e))
            time.sleep(1)
        return False

    def find_wifi(self, str):
        self.printLog("Finding wifi %s  ..."%str)
        p = subprocess.Popen("netsh wlan disconnect",shell=True)# win10 system cannot auto refresh wifi list, so disconnect it first
        p.wait()
        #p = os.popen("netsh wlan show networks") #netsh wlan show networks mode=bssid
        #content = p.read().decode("gbk", "ignore")
        p = subprocess.Popen("netsh wlan show networks | find \"%s\""%str,shell=True,stdout=subprocess.PIPE)
        try:
            content = p.stdout.read().decode("GB2312") # byte decode to str, and GB2312 is avoid Chinese strings.
        except:
            content = p.stdout.read().decode("utf-8")
        if content != "":
            self.printLog("Find [%s]"%str)
            return True
        else:
            return False

if __name__=="__main__":
    wifi = windowsWifi()
    data = wifi.find_wifi("Beoplay M3_00094760")
    print(data)
