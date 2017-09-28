#coding = utf-8
#Author: Bruce.Zhu

import configparser
import time
import re
import sys
import urllib.request
from src.common.aseInfo import aseInfo
from src.common.logger_config import logger
from src.common.windowsWifi import windowsWifi
from src.common.database import *
from src.common.ase_finder import deviceScan

class wifiSetup:
    def __init__(self, framelogPrint, infoPage, btnRefresh, labelStatus, listBoxDeviceName, messagebox):
        self.framelogPrint = framelogPrint
        self.wifi = windowsWifi(framelogPrint)
        self.ase_info = aseInfo()
        self.deviceScan = deviceScan(infoPage, btnRefresh, labelStatus, listBoxDeviceName, messagebox)
        self.total_times = 0
        self.success_times = 0

    def printLog(self, info):
        try:
            self.framelogPrint.addLog(info, ' ')
        except Exception as e:
            logger.debug("Error when printLog: {}".format(e))
            sys.exit()
    
    def reset_and_wait(self, ip, Time):
        self.ase_info.reset(ip)
        self.printLog("Do factory reset. Waiting %ss..."%Time)
        time.sleep(Time)        
    
    def check_wifi_status(self, ip):
        try:
            response = urllib.request.urlopen(ip, timeout=20)
            status = response.status
            if status == 200:
                return True
            else:
                return False 
        except Exception as e:
            self.printLog("Cannot connect {}: {}".format(ip, e))
            return False    
    
    def setup(self, orginalIp):
        productName = SQL("select productname from scanase where ip='{}'".format(orginalIp))[0][0]
        try:
            conf = configparser.ConfigParser()
            conf.read(".\\wifiSetting.ini")
            
            times = conf.getint("Run", "times")
            time_reset = conf.getint("Run", "time_reset")
            
            dhcp = conf.get("Wifi", "dhcp")
            ssid = conf.get("Wifi", "ssid")
            key = conf.get("Wifi", "key")
            encryption = conf.get("Wifi", "encryption")
            ip = conf.get("Wifi", "ip")
            gateway = conf.get("Wifi", "gateway")
            netmask = conf.get("Wifi", "netmask")
        except Exception as e:
            logger.error(e)
            return
        #hostName = "beoplay-{model}-{SN}.local".format(model=model, SN=SN)
        hostUrl = "http://{}/index.fcgi"
        
        self.framelogPrint.labelShowDHCP['text'] = dhcp
        DHCP = []
        if dhcp == "True" or dhcp == "true":
            DHCP.append(True)
        elif dhcp == "False" or dhcp == "false":
            DHCP.append(False)
        else:
            DHCP.extend([True, False, True])
        self.total_times = times
        self.framelogPrint.labelShowTotalTimes['text'] = self.total_times
        
        for cycle in range(1,times+1):
            self.printLog("This is the %d times "%cycle+"*"*30)
            for index in DHCP:
                self.printLog("\n")
                dhcp = index
                self.printLog("Set DHCP={}".format(dhcp))
                self.reset_and_wait(orginalIp, time_reset)
                while True:
                    if self.wifi.find_wifi(productName):
                        self.wifi.connect_wifi(productName)
                        time.sleep(15)#Give wifi connect some time
                        if self.wifi.check_wifi(productName):
                            break
                    time.sleep(3)
                    
                if self.check_wifi_status("http://192.168.1.1/index.fcgi#Fts/Network") == False: return        
                if self.ase_info.setupWifi(ssid, key, encryption, dhcp, ip, gateway, netmask, "192.168.1.1"):
                    self.printLog("Wifi setup command has been sent!")
                    if self.wifi.find_wifi(ssid):
                        self.wifi.connect_wifi(ssid)
                        time.sleep(15)#Give wifi connect some time
                        if self.wifi.check_wifi(ssid):
                            self.deviceScan.scan()
                            find = True
                            find_times = 0
                            while find:
                                find_times += 1
                                self.printLog("Start finding device {} times".format(find_times))
                                if find_times > 6:
                                    self.printLog("Cannot discover your DUT[{}] on Wifi[{}]".format(productName,ssid))
                                    return
                                status = 1
                                while status==1:
                                    try:
                                        status = SQL("select status from STATUS where SCAN='ase_scan'")[0][0]
                                    except Exception as e:
                                        time.sleep(2)
                                        logger.error(e)
                                        status=1
                                devices = SQL("select productname from SCANASE")
                                for device in devices:
                                    deviceName = device[0]
                                    if deviceName == productName:
                                        orginalIp = SQL("select ip from SCANASE where productname='{}'".format(deviceName))[0][0]
                                        find = False
                                        break
                            if self.check_wifi_status(hostUrl.format(orginalIp)):
                                if not dhcp:
                                    if ip == orginalIp:
                                        self.printLog("Your static ip[{}] setup successfully!".format(ip))
                                    else:
                                        self.printLog("Your static ip[{}] setup Failed!".format(ip))
                                        return
                                else:  
                                    self.printLog("Wifi[{}] setup successfully!".format(ssid))
                                self.success_times = self.success_times + 1
                        else:
                            self.printLog("Cannot connect wifi %s"%TestWifi)
                            break
                
                self.framelogPrint.labelShowSuccesTimes['text'] = self.success_times
            if self.success_times >= self.total_times:
                finish_print = "\n*******************************\n**********All finished*********\n*******************************\n"
                self.printLog(finish_print)
