# -*- coding: utf-8 -*-
'''
Created on 2016.10

@author: bruce.zhu
'''
import os
import datetime
import time
#import requests
import urllib.request
import configparser
import sys

#from src.common.createHTMLReport import *
from src.common.logger_config import logger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class aseUpdate:

    def __init__(self, ip, modelName, framelogPrint):
        self.framelogPrint = framelogPrint
        try:
            conf = configparser.ConfigParser()
            conf.read('.\\src\\config\\aseUpdate.ini')
            #parent_path = os.path.realpath(os.path.join(os.getcwd(), ".."))
            self.low_version_path = '{}'.format(conf.get("Firmware", "low_version_path")) #avoid path contains empty strings
            self.high_version_path = '{}'.format(conf.get("Firmware", "high_version_path"))
            self.low_version = conf.get("Firmware", "low_version").replace(' ', '')
            self.high_version = conf.get("Firmware", "high_version").replace(' ', '')
            self.cycle = conf.getint("Running_times", "times")
            self.IP = "http://{}".format(ip)
            self.title = modelName + " auto update OTA Test"
        except Exception as e:
            self.printLog(e)
            sys.exit()

        self.shot_path = ''
        self.pageTimeout = 15
        self.update_times = 0
        self.downgrade_times = 0
        self.Network_Error = 0
        #driver = webdriver.Chrome("%s\chromedriver2.9.exe"%os.getcwd())
        self.printLog("Start to Auto Update Test!")
        try:
            self.printLog("Open Setting Page by browser Firefox...")
            self.driver = webdriver.Firefox()
            self.driver.get(self.IP)
        except Exception as e:
            self.printLog(e)
        #s = unicode ("成 ", "utf-8")

    def printLog(self, info):
        try:
            self.framelogPrint.addLog(info, ' ')
        except Exception as e:
            logger.debug("Error when printLog: {}".format(e))
            self.driver.quit()
            sys.exit()

    def screenshot(self, info):
        self.printLog("%s\%s_%s.jpg"%(self.shot_path,info,time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) ))
        self.driver.get_screenshot_as_file("%s/%s_%s.jpg"%(self.shot_path,info,time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) ))

    def check_network(self, url):
        try:
            #r = requests.get(url, allow_redirects = False)
            #status = r.status_code
            r = urllib.request.urlopen(url, timeout = 8)
            status = r.getcode()
            if status == 200:
                self.printLog('Network is ok')
                return True
            else:
                self.screenshot("Network error")
                logging.log(logging.ERROR, 'Network error!!!!')
                return False
        except:
            self.screenshot("Network error")
            logging.log(logging.ERROR, 'Network error!!!!')
            return False

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #make screen shot directory
    def make_shot_dir(self):
        #shot_conf = dict(root_run = os.getcwd())
        run_shot_dir = os.path.realpath(os.path.join(os.getcwd(), ".", 'shot'))

        if not os.path.exists(run_shot_dir):
            os.makedirs(run_shot_dir)

        return run_shot_dir
        #shot_conf['runshot_dir'] = run_shot_dir
        #return shot_conf

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def switch_frame(self, frame_type):
        try:
            if frame_type == "default":
                self.driver.switch_to_default_content()
            elif frame_type == "rightFrame":
                self.driver.switch_to_frame("rightFrame")
            elif frame_type == "leftFrame":
                self.driver.switch_to_frame("leftFrame")
            else:
                self.printLog("No such frame {}".format(frame_type))
        except NotImplementedError as e:
            self.printLog(e)
            return False
        else:
            return True

    def find_element(self, ele_type, timeout, value):
        """
        Args:
            ele_type(str): element type
            timeout(int): max time at finding element
            value(str): element attribute value
        Returns:
            ele(WebElement): return object of found element
        """
        ele = None
        try:
            if ele_type == "id":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_id(value))
                ele = self.driver.find_element_by_id(value)
            elif ele_type == "name":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_name(value))
                ele = self.driver.find_element_by_name(value)
            elif ele_type == "class_name":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_class_name(value))
                ele = self.driver.find_element_by_class_name(value)
            elif ele_type == "link_text":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_link_text(value))
                ele = self.driver.find_element_by_link_text(value)
            elif ele_type == "partial_link_text":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_partial_link_text(value))
                ele = self.driver.find_element_by_partial_link_text(value)
            elif ele_type == "tag_name":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_tag_name(value))
                ele = self.driver.find_element_by_tag_name(value)
            elif ele_type == "xpath":
                WebDriverWait(self.driver, timeout).until(lambda driver: driver.find_element_by_xpath(value))
                ele = self.driver.find_element_by_xpath(value)
            else:
                self.printLog("No such locate element way {}".format(ele_type))
        except NotImplementedError as e:
            self.printLog(e)
        except TimeoutError as e:
            logging.log(logging, e)
            sys.exit()
        #else:
            #return ele
        finally:
            return ele
        """
        repeat = 10
        i = 0
        for i in range(1,repeat+1):
            try:
                driver.find_element_by_xpath(element)
                break
            except:
                self.printLog("Try to find %s  ----%s times!"%(element,i))
                time.sleep(1)

        if i==repeat:
            self.printLog("Can not find relevant element [%s]! Please check your network!"%element)
            self.printLog("Please restart test!.............")
            screenshot("Cannot_find_element")
            sys.exit()
            return

        return driver.find_element_by_xpath(element)
        """
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def update_percentage(self):
        time.sleep(20)
        """
        f=0
        while f==0:
            time.sleep(2)
            if check_popup():

                driver.switch_to_frame("rightFrame")
                try:
                    str_per=find_element("//*[@id='DownloadProgressMsg']").text #Firmware upload status: 42% completed.
                    print "english"
                except:
                    time.sleep(0.5)
                '''
                try:
                    str_per=find_element("//*[@id='ProgressMsg']").text #固件上传状态：完成 XX%   //*[@id="ProgressMsg"]
                    print "chinese"
                except:
                    time.sleep(0.5)
                '''
                print str_per
                if "Firmware" in str_per:
    				a,b = str_per.split(": ")
    				c,d = b.split("%")
    				per = c
                else: #<div id="ProgressMsg" class="Bo-text">固件上传状态：完成 50%。</div>
    				a,b = str_per.split(s)
    				c,d = b.split("%")
    				per = c
                if int(per)>85: #variable per must turn to integer
                    f=1
                    print per
                    time.sleep(10)
            else:
                return False
        """
        f=0
        while f==0:
            #stime.sleep(8)
            if self.check_popup()==False:
                self.switch_frame("default")
                self.switch_frame("rightFrame")
                try:
                    #print find_element("//*[@id='ConfirmUpdateDone']").text
                    ConfirmUpdateDone = self.find_element("xpath",10,"//*[@id='ConfirmUpdateDone']")
                    ConfirmUpdateDone.click()
                    f=1
                    return True
                except Exception as e:
                    #logger.debug(e)
                    f=0
            else:
                return False
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def check_version(self, v):
        self.switch_frame("default")
        self.switch_frame("rightFrame")
        softwareVersion = self.find_element("xpath", self.pageTimeout,"//*[@id='softwareVersion']")
        if softwareVersion == None:
            return False
        version = softwareVersion.text
        self.printLog("DUT current version is %s"%version)
        if v == version:
            #success_time=success_time+1
            self.printLog("Update success!")
            return True
        else:
            self.printLog("Update fail!")
            return False
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def check_popup(self):
        """Check popup box when Uploading or updatings
        Returns:
                True: Appear popup
                False: No popup
        """
        self.switch_frame("default")
        try:
            popup = self.find_element("class_name", 1, "imgButtonYes")
            popup.is_displayed()
            #driver.find_element_by_class_name("imgButtonYes").is_displayed()
            self.screenshot("%s_popup"%self.Network_Error)
            popup.click()
            self.printLog("Network unavailable")
            self.Network_Error+=1
            return True
        except:
            return False
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def agreementPage(self):
        time.sleep(5)
        self.switch_frame("default")
        self.switch_frame("rightFrame")
        logger.debug('Checking if there is agreement page!')
        if self.find_element("xpath", self.pageTimeout, "//*[@id='BtnOK1']") == None:
            return
        logger.debug('Start to click agreement page!')
        self.find_element("xpath", self.pageTimeout, "//*[@id='BtnOK1']").click()
        time.sleep(3)
        self.find_element("xpath", self.pageTimeout, "//*[@id='BtnOK2']").click()
        time.sleep(3)
        self.switch_frame("default")
        self.switch_frame("rightFrame")
        self.find_element("xpath", self.pageTimeout, "//*[@id=\"Accept\"]").click()
        time.sleep(3)
        self.find_element("xpath", self.pageTimeout, "//*[@id='NoThanks']").click()
        time.sleep(7)

    def update_local(self, local_file, version):
        self.switch_frame("rightFrame")

        time.sleep(1)
        LocalUpdateButton = self.find_element("xpath", self.pageTimeout, "//*[@id='LocalUpdateButton']")
        LocalUpdateButton.click()

        time.sleep(3)
        datafile = self.find_element("xpath", self.pageTimeout, "//*[@id='datafile']")
        datafile.send_keys('%s'%local_file)

        time.sleep(3)
        LoadFileButton = self.find_element("xpath", self.pageTimeout, "//*[@id='LoadFileButton']")
        LoadFileButton.click()

        self.printLog("Uploading %s file..."%local_file)
        f=0 #If uploading success, f=1, end while
        while f==0:
            time.sleep(5)
            if self.check_popup() == False:
                self.switch_frame("rightFrame")
                #NewSWVersion = self.find_element("xpath", self.pageTimeout, "//*[@id='NewSWVersion']")
                #version_name = NewSWVersion.text
                try:
                    LocalUpdateConfirmYes = self.find_element("xpath", self.pageTimeout, "//*[@id='LocalUpdateConfirmYes']")
                    LocalUpdateConfirmYes.click()
                    self.printLog("Uploading success!")
                    self.printLog("Start burn into...!")
                    f = 1
                except:
                    logger.debug('Wait for Yes button')

                #print('*', end = '')
                """
                if version_name != "":
                    print(version_name)
                    if version_name==version:
                        self.printLog("Uploading success!")
                        time.sleep(10)

                        LocalUpdateConfirmYes = find_element("//*[@id='LocalUpdateConfirmYes']")
                        LocalUpdateConfirmYes.click()

                        self.printLog("Start burn into...!")
                        f=1
                    else:
                        self.printLog("Version %s does not matchself.low_version %s, please check your config.ini!"%(version_name,self.low_version))

                """
            else:
                return False
        if self.update_percentage()==False:
            return False

        return True

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def update_server(self):
        local_file = self.low_version_path
        if current_version==self.high_version:
            self.printLog("Downgrade on local")

            self.update_local(local_file, self.low_version)
            time.sleep(10)
            if self.check_version(self.low_version):
                self.printLog("Downgrade success from %s to version %s on local"%(self.high_version,self.low_version))
                self.downgrade_times+=1

        else:
            self.printLog("Update on server")
            time.sleep(2)
            self.switch_frame("rightFrame")

            f=0 #If uploading success, f=1, end while
            while f==0:
                if self.check_popup()==False:
                    self.switch_frame("rightFrame")
                    #self.driver.switch_to_frame("rightFrame")
                    NewSWVersion = self.find_element("xpath", self.pageTimeout, "//*[@id='NewSWVersion']")
                    check_nv = NewSWVersion.text #check new version
                    if check_nv == self.high_version:
                        UpdateFromNetworkButton = self.find_element("xpath", self.pageTimeout, "//*[@id='UpdateFromNetworkButton']")
                        UpdateFromNetworkButton.click()
                        time.sleep(3)
                        NetworkUpdateConfirmYes = self.find_element("xpath", self.pageTimeout, "//*[@id='NetworkUpdateConfirmYes']")
                        NetworkUpdateConfirmYes.click()
                        self.printLog("Start update!")
                        f=1
                else:
                    return False
            if self.update_percentage()==False:
                return False
            time.sleep(10)
            if self.check_version(self.high_version):
                self.printLog("Update success from %s to version %s on internet"%(self.low_version,self.high_version))
                self.update_times+=1
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def update_full(self):
        self.printLog(self.driver.title+"("+self.IP+")")

        self.agreementPage()

        time.sleep(2)
        self.switch_frame("default")
        self.switch_frame("rightFrame")

        softwareVersion = self.find_element("xpath", self.pageTimeout, "//*[@id='softwareVersion']")
        current_version = softwareVersion.text

        self.printLog("DUT current version is %s"%current_version)
        ## Switch back to main window
        self.switch_frame("default")

        time.sleep(2)
        self.switch_frame("leftFrame")
        SwUpdatePage = self.find_element("xpath", self.pageTimeout, "//*[@id='SwUpdatePage']/span")
        SwUpdatePage.click()

        self.switch_frame("default")

        if (current_version!=self.low_version) and (current_version!=self.high_version):
            self.update_local(self.high_version_path, self.high_version)
            time.sleep(10)
            self.check_version(self.high_version)
            return

        if self.low_version_path == self.high_version_path:
            update_server()

        #**************************************************************************************************************
        else:
            if current_version==self.high_version:
                local_file = self.low_version_path
                versionCheck = self.low_version
                self.printLog("Downgrade to version %s just with local file"%versionCheck)
            else:
                local_file = self.high_version_path
                versionCheck = self.high_version
                self.printLog("Update to version %s just with local file"%versionCheck)

            self.update_local(local_file, versionCheck)
            time.sleep(10)
            if self.check_version(versionCheck):
                if versionCheck==self.low_version:
                    self.printLog("Downgrade success from %s to version %s on local"%(self.high_version,self.low_version))
                    self.downgrade_times+=1
                elif versionCheck==self.high_version:
                    self.printLog("Update success from %s to version %s on internet"%(self.low_version,self.high_version))
                    self.update_times+=1
                else:
                    logging.log(logging.ERROR, "No such version! Error")

    def startOTA(self):
        Run_status = "Running"
        update = "Update success from %s to version %s on internet"%(self.low_version,self.high_version)
        downgrade = "Downgrade success from %s to version %s on local"%(self.high_version,self.low_version)
        self.shot_path = self.make_shot_dir()

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        start = time.time()
        self.framelogPrint.labelShowStartTime['text'] = start_time
        self.framelogPrint.labelShowRuntimes['text'] = self.cycle

        i=1
        for i in range(1, self.cycle+1):
            self.printLog("This is %i times----------------------------------------"%i)
            for j in range(0,2):
                if self.check_network(self.IP+"/index.fcgi"):
                    #when version file have been download from server(on updating),but the net disconnect
                    if self.update_full() == False:
                        self.printLog("Maybe Network trouble, so wait 100 second, then open setting page again")
                        time.sleep(100)#why is 100s, as sometimes, update still can go on by DUT self
                        self.driver.quit()
                        self.driver = webdriver.Chrome("%s\chromedriver.exe"%os.getcwd())
                        self.driver.get(self.IP)
                    if i == self.cycle:
                        Run_status="Running Over"
                    end = time.time()
                    diff_time = int(end-start)
                    #duration="%sh:%sm:%ss"%(int((end-start)/3600),int((end-start)/60),int((end-start)%60))
                    duration = str(datetime.timedelta(seconds=diff_time))
                    #self.printLog("Success update times is %d"%self.update_times)
                    self.framelogPrint.labelShowElapsedTime['text'] = duration
                    self.framelogPrint.labelShowNetworkError['text'] = '{}'.format(self.Network_Error)
                    self.framelogPrint.labelShowPass['text'] = '{0}/{1}(Upgrade) {2}/{3}(Downgrade)'.format(self.update_times,  i, self.downgrade_times, i)
                    #CreateHTMLRpt.report_result(self.title,start_time,duration,str(i),Run_status,update,str(self.update_times),downgrade,str(self.downgrade_times),'self.Network_Error',str(self.Network_Error))

        self.driver.quit()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Main()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__=='__main__':
    update = aseUpdate()
    update.startOTA()
