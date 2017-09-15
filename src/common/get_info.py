"""
Created on Jan 3, 2017

@author: Bruce zhu
"""
import urllib.request
import time
import re
import logging
import json

class device_status:

    def __init__(self):
        self.ip = 'NA'
        self.device = 'NA'

    def get_url(self, url):
        try:
            data = urllib.request.urlopen(url, timeout=8)
            text = data.read().decode('utf8')
            data.close()
            self.timeCount = 0
            return text
        except:
            return 'NA'

    def status_static(self, x, ip):
        self.ip = ip
        self.device_source_url = 'http://' + self.ip + '/api/getData?path=sources%3Alist&roles=value&'
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
            if x == 'device_name':
                self.device_name_url = 'http://' + self.ip + '/api/getData?path=settings%3A%2FdeviceName&roles=value'
                deviceName = json.loads(self.get_url(self.device_name_url), encoding='utf-8')
                device_name = deviceName[0]['string_']
                return device_name
            if x == 'device_version':
                self.device_version_url = 'http://' + self.ip + '/api/getData?path=%2Fsystem%2FdisplayVersion&roles=value&'
                return re.findall('string_":"(.+)","type', self.get_url(self.device_version_url))[0]
            if x == 'wifi_device':
                self.device_wifi_url = 'http://' + self.ip + '/api/getData?path=networkWizard%3Ainfo%2FWirelessSSID&roles=value'
                return re.findall('string_":"(.+)",', self.get_url(self.device_wifi_url))[0]
            if x == 'wifi_level':
                self.wifi_level_url = 'http://' + self.ip + '/api/getData?path=settings%3Abeo%2FwifiSignalLevel&roles=value&'
                return re.findall(':\\[(.+)\\]}', self.get_url(self.wifi_level_url))[0]
            if x == 'volume_default':
                self.volume_default_url = 'http://' + self.ip + '/api/getData?path=settings%3A%2FmediaPlayer%2FvolumeDefault&roles=value&'
                return re.findall('i32_":(.+),"', self.get_url(self.volume_default_url))[0]
            if x == 'volume_max':
                self.volume_max_url = 'http://' + self.ip + '/api/getData?path=settings%3A%2FmediaPlayer%2FvolumeMax&roles=value&'
                return re.findall('i32_":(.+),"', self.get_url(self.volume_max_url))[0]
            if x == 'bt_open':
                self.bt_open_url = 'http://' + self.ip + '/api/getData?path=settings%3A%2Fbluetooth%2FpairingAlwaysEnabled&roles=value&'
                if re.findall('bool_":(.+),"type', self.get_url(self.bt_open_url))[0] == 'true':
                    return True
                else:
                    return False
            elif x == 'bt_connectWay':
                self.bt_connectWay_url = 'http://' + self.ip + '/api/getData?path=settings%3A%2Fbluetooth%2FautoConnect&roles=value&'
                str_connectWay = re.findall('Mode":"(.+)"}', self.get_url(self.bt_connectWay_url))[0]
                if str_connectWay == 'manual':
                    return 'Manual'
                elif str_connectWay == 'automatic':
                    return 'Automatic'
                else:
                    return 'Disable'
            else:
                if x == 'bt':
                    self.device_btpaired_url = 'http://' + self.ip + '/api/getRows?path=bluetooth%3ApairedPlayers&roles=title%2Cid%2Cdescription&from=0&to=99'
                    resp_value = self.get_url(self.device_btpaired_url)
                    data = json.loads(resp_value, encoding='GBK')  #Avoid chinese strings
                    return data
                    return self.bt
                return 'NA'
        except Exception as e:
            logging.log(logging.DEBUG, 'cmd = {0}, error: {1}'.format(x, e))
            return 'NA'

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