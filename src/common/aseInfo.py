"""
Created on Jan 3, 2017

@author: Bruce zhu
"""
import urllib.request
import time
import re
import json

from src.common.logger_config import logger
from src.common.aseWebData import *

class aseInfo:

    def __init__(self):
        self.ip = 'NA'
        self.device = 'NA'
        self.urlSetData = "http://{}/api/setData?{}"
        self.urlGetData = "http://{}/api/getData?{}"
        self.urlGetRows = "http://{}/api/getRows?{}"

    def get_url(self, url):
        try:
            data = urllib.request.urlopen(url, timeout=8)
            text = data.read().decode('utf8')
            data.close()
            self.timeCount = 0
            return text
        except:
            return 'NA'

    def transferData(self, request_way, ip, value):
        valueStr = urllib.parse.urlencode(value, encoding="utf-8")
        if "+" in valueStr:
            valueStr = valueStr.replace('+', '')
        if "True" in valueStr:
            valueStr = valueStr.replace('True', 'true')
        if "False" in valueStr:
            valueStr = valueStr.replace('False', 'false')
        if "%27" in valueStr:
            valueStr = valueStr.replace('%27', '%22')
        if request_way == "get":
            url = self.urlGetData.format(ip, valueStr)
            return self.get_url(url)
        elif request_way == "getRows":
            url = self.urlGetRows.format(ip, valueStr)
            return self.get_url(url)            
        elif request_way == "post":
            url = self.urlSetData.format(ip, valueStr)
            self.get_url(url)
        else:
            logger.info("No such request way: {}".format(request_way))
                        
    def get_info(self, x, ip):
        self.ip = ip
        try:
            if x == 'basicInfo':
                resp_value = self.get_url('http://{0}/index.fcgi'.format(self.ip))
                data = re.findall('dataJSON = .*', resp_value)[0]
                data = data.replace(data[-2:], '')
                data = data.replace(data[:12], '')
                data = json.loads(data, encoding='utf-8')
                info = {}
                info['modelName'] = data['beoMachine']['modelName']
                info['model'] = data['beoMachine']['model']
                info['productName'] = data['beoMachine']['setup']['productName']
                info['bootloaderVersion'] = data['beoMachine']['fepVersions']['bootloaderVersion']
                info['appVersion'] = data['beoMachine']['fepVersions']['appVersion']
                return info
            elif x == 'device_name':
                data = self.transferData("get", ip, deviceName_para)
                deviceName = json.loads(data, encoding='utf-8')
                device_name = deviceName[0]['string_']
                return device_name
            elif x == 'device_version':
                data = self.transferData("get", ip, displayVersion_para)
                data = json.loads(data, encoding='utf-8')
                return data[0]["string_"]
            elif x == 'wifi_device':
                data = self.transferData("get", ip, WirelessSSID_para)
                data = json.loads(data, encoding='utf-8')
                return data[0]["string_"]
            #elif x == 'wifi_level':
            #    data = self.transferData("get", ip, wifiSignalLevel_para)
            #    return re.findall(':\\[(.+)\\]}', data)[0]
            elif x == 'volume_default':
                data = self.transferData("get", ip, volumeDefault_para)
                data = json.loads(data, encoding='utf-8')
                return data[0]["i32_"]
            elif x == 'volume_max':
                data = self.transferData("get", ip, volumeMax_para)
                data = json.loads(data, encoding='utf-8')
                return data[0]["i32_"]
            elif x == 'bt_open':
                data = self.transferData("get", ip, pairingAlwaysEnabled_para)
                data = json.loads(data, encoding='utf-8')
                return data[0]["bool_"]
            elif x == 'bt_reconnect':
                data = self.transferData("get", ip, autoConnect_para)
                data = json.loads(data, encoding='utf-8')
                connectMode = data[0]["bluetoothAutoConnectMode"]
                if connectMode == 'manual':
                    return 'Manual'
                elif connectMode == 'automatic':
                    return 'Automatic'
                else:
                    return 'Disable'
            elif x == 'bt':
                data = self.transferData("getRows", ip, pairedPlayers_para)
                value = json.loads(data, encoding='GBK')  #Avoid chinese strings
                return value
            else:
                return 'NA'
        except Exception as e:
            logger.debug('cmd = {0}, error: {1}'.format(x, e))
            return 'NA'

    def scanWifi(self, ip):
        data = self.transferData("getRows", ip, network_scan_results_para)

    def pairBT(self, pair, ip):
        if pair == 'pair':
            para = pairBT_para
        elif pair == 'cancel':
            para = pairCancelBT_para
        self.transferData("post", ip, para)
        
    def reset(self, ip):
        self.transferData("post", ip, factoryResetRequest_para)

    def change_product_name(self, name, ip):
        self.transferData("post", ip, set_deviceName_para(name))
        
    def bt_open_set(self, open_enable, ip):
        self.transferData("post", ip, set_pairingAlwaysEnabled(open_enable))
        
    def bt_reconnect_set(self, status, ip):
        if status == 'Manual':
            mode = 'manual'
        elif status == 'Automatic':
            mode = 'automatic'
        elif status == 'Disable':
            mode = 'none'
        else:
            return
        self.transferData("post", ip, set_autoConnect(mode))
    
    def status_dynamic(self, x, ip):
        self.ip = ip
        self.device_volume_url = 'http://' + self.ip + '/api/getData?path=BeoSound%3A%2Fvolume&roles=value&'
        self.device_battery = 'http://' + self.ip + '/api/getData?path=power%3AenergyState&roles=value&'
        try:
            if x == 'volume_current':
                return re.findall('i32_":(.+),', self.get_url(self.device_volume_url))[0]
            if x == 'batteryPercentage':
                return re.findall('batteryPercentage":(\\d+),', self.get_url(self.device_battery))[0]
            if x == 'batteryHealthStatus':
                return re.findall('batteryHealthStatus":"(.+)","batteryStatus', self.get_url(self.device_battery))[0]
            if x == 'batteryStatus':
                return re.findall('batteryStatus":"(.+)","timestamp', self.get_url(self.device_battery))[0]
            return 'NA'
        except:
            return 'NA'
        
    def setupWifi(self, ssid="", key="", encryption="wpa_psk", dhcp=True, ip="", gateway="", netmask="", originalIp=""):
        #logging.log(logging.INFO, "Setup wifi ssid=%s key=%s"%(wifissid,pwd))
        wireless = {"dhcp":dhcp,
                    "dns":["",""],
                    "gateway":gateway,
                    "encryption":encryption,
                    "ip":ip,
                    "ssid":ssid,
                    "netmask":netmask,
                    "key":key}
        wired = {"dhcp":dhcp,
                "dns":["",""],
                "gateway":"",
                "ip":"",
                "netmask":""}
        networkProfile = {"wireless":wireless,
                        "wired":wired,
                        "type":"automatic",}                        
        value = {"networkProfile":networkProfile,
                "type":"networkProfile",}
        wifi_value = {"path":"BeoWeb:/network", "roles":"activate",
                      "value":value}
        try:
            self.transferData("post", originalIp, wifi_value)
        except Exception as e:
            logger.info(e)
            return False
        else:
            return True
            
    
