# -*- coding: utf-8 -*-
from time import *
from .PyTkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
#-----------------------------------
import os
import re
import threading
import subprocess
import sys
import logging
import configparser
import _thread
import webbrowser
#-----------------------------------
from src.ui.appUpdate import appUpdate
from src.common.get_info import device_status
from src.common.clearLogs import clearLogs
from src.common.ase_finder import deviceScan
from .FrameUpdateSet import FrameUpdateSet
#-----------------------------------
#-----------------------------------
dev_status = device_status()

monaco_font = ('Monaco', 12)
font = monaco_font
size_dict = dict()
size_dict = {
                "list_box_height": 19,
                "send_text_height": 12,
                "receive_text_height": 15,
                "reset_label_width": 24,
                "clear_label_width": 22
            }

conf = configparser.ConfigParser()
try:
    conf.read('./src/config/version.ini')
    appVerson = conf.get("version", "app")
except Exception as e:
    logging.log(logging.DEBUG, 'Error: {0}'.format(e))
    sys.exit()

class MainFrame:

    def __init__(self, logfilename):

        self.root = tk.Tk()
        self.title = "Wifi Speaker v{0} SQA".format(appVerson)
        self.icon = "%s\\src\\config\\icon\\sound_speaker_48px.ico"%os.getcwd()
        self.create_frame()
        #--------------------------------
        self.deviceName = 'NA'
        self.ip = 'NA'
        self.device = 'NA'
        self.infoStart = 0
        self.backFlag = 0 # default is left frame

        self.infoPage = 0
        self.modelName = ''

        #thread
        _thread.start_new_thread(deviceScan(self.infoPage, self.labelStatus, self.__listBoxDeviceName, messagebox).scan, ())
        #self.refresh_static()
        #self.refresh_dynamic()
        #self.refresh_temperature()
        #self.refresh_aseinfo()

        _thread.start_new_thread(clearLogs(messagebox, logfilename).clearLog, ())

    def mainLoop(self):
        self.__setupRoot()
        self.root.mainloop()

    def __setupRoot(self):
        # setup root
        if g_default_theme == "dark":
            self.root.configure(bg="#292929")
            combostyle = ttk.Style()
            combostyle.theme_use('alt')
            combostyle.configure("TCombobox", selectbackground="#292929", fieldbackground="#292929",
                                              background="#292929", foreground="#FFFFFF")
        self.root.resizable(False, False)
        self.root.title(self.title)
        self.root.iconbitmap(self.icon)
        #self.root.protocol('WM_DELETE_WINDOW', lambda:0) #ignore close

    def create_frame(self):
        self.menu_bar = tk.Frame(self.root, borderwidth=2)
        self.frm = PyLabelFrame(self.root)
        self.frm_status = PyLabelFrame(self.root)

        self.menu_bar.grid(row=0, column=0, padx=0, pady=0, sticky="we")
        self.frm.grid(row=1, column=0, sticky="wesn")
        self.frm_status.grid(row=2, column=0, sticky="wesn")

        help_menu = self.create_help_menu()
        #about_menu = self.create_about_menu()
        tools_menu = self.create_tools_menu()
        self.menu_bar.tk_menuBar(help_menu, tools_menu)
        self.create_frm()
        self.create_frm_status()

    #===================================================================================
    def create_help_menu(self):
        HELP_MENU_ITEMS = ['Undo', 'How to use', 'About']
        help_item = tk.Menubutton(self.menu_bar, text='Help', underline=1)
        help_item.pack(side='left', padx='1m')
        help_item.menu = tk.Menu(help_item)

        help_item.menu.add('command', label=HELP_MENU_ITEMS[0])
        help_item.menu.entryconfig(1, state='disabled')

        help_item.menu.add_command(label=HELP_MENU_ITEMS[1])
        help_item.menu.add_command(label=HELP_MENU_ITEMS[2], command=self.about)
        help_item['menu'] = help_item.menu
        return help_item

    def create_tools_menu(self):
        TOOLS_MENU_ITEMS = ['Check for Updates']
        tools_item = tk.Menubutton(self.menu_bar, text='Tools', underline=1)
        tools_item.pack(side='left', padx='1m')
        tools_item.menu = tk.Menu(tools_item)
        tools_item.menu.add_command(label=TOOLS_MENU_ITEMS[0], command=self.checkForUpdates)
        tools_item['menu'] = tools_item.menu
        return tools_item

    def about(self):
        messagebox.showinfo('About', 'Versoin: {0}\nAuthor: Bruce Zhu\nEmail: bruce.zhu@tymphany.com'.format(appVerson))

    def checkForUpdates(self):
        checkUpdate = appUpdate(self.root, messagebox)
        checkUpdate.checkForUpdates()

    def create_frm(self):
        '''
        Top part divided into left and right part
        '''
        self.frm_left = PyLabelFrame(self.frm)
        self.frm_right = PyLabelFrame(self.frm)

        self.frm_left.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        #self.frm_right.grid(row=0, column=1, padx=5, pady=5, sticky="wesn")

        self.create_frm_left()
        self.create_frm_right()

    def create_frm_left(self):
        self.frm_left_up = PyLabelFrame(self.frm_left)
        self.frm_left_down = PyLabelFrame(self.frm_left)

        self.frm_left_up.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_left_down.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")

        self.create_frm_left_up()
        self.create_frm_left_down()

    def create_frm_left_up(self):
        self.frm_left_label = PyLabel(self.frm_left_up,
                                           text="Device Scan:                                      ",
                                           font=font)
        self.__listBoxDeviceName = PyListbox(self.frm_left_up,
                                                   height=size_dict["list_box_height"],
                                                   font=font)

        self.frm_left_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        self.__listBoxDeviceName.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")
        self.__listBoxDeviceName.bind('<Double-Button-1>', self.__onlistSelectBtnClick)

    def create_frm_left_down(self):
        self.btnRefresh = PyButton(self.frm_left_down,
                                          text="Refresh",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnRefresh)

        self.frm_left_down_labelEmpty = PyLabel(self.frm_left_down,
                                           text=" "*14,
                                           font=font)
        self.inputIPStr = tk.StringVar()
        self.entryInputIp = PyEntry(self.frm_left_down,
                                            textvariable=self.inputIPStr,
                                            width=15,
                                            font=font)

        self.btnInputIP = PyButton(self.frm_left_down,
                                          text="Input IP",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnInputIP)

        self.btnRefresh.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.frm_left_down_labelEmpty.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entryInputIp.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.btnInputIP.grid(row=0, column=3, padx=5, pady=5, sticky="e")

    def create_frm_right(self):
        self.frm_right_title = PyLabelFrame(self.frm_right)
        self.frm_right_information = PyLabelFrame(self.frm_right)
        self.frm_right_operation = PyLabelFrame(self.frm_right)
        self.frm_right_page = PyLabelFrame(self.frm_right)

        self.frm_right_title.grid(row=0, column=0, padx=1, sticky="wesn")
        self.frm_right_information.grid(row=1, column=0, padx=1, sticky="wesn")
        self.frm_right_operation.grid(row=2, column=0, padx=1, sticky="wesn")
        self.frm_right_page.grid(row=3, column=0, padx=1, sticky="wesn")

        self.create_frm_right_title()
        self.create_frm_right_information()
        self.create_frm_right_operation()
        self.create_frm_right_page()

    def create_frm_right_title(self):
        #self.labelTitle = PyLabel(self.frm_right_title,text= '         ',font=font)
        self.labelTitle = PyLabel(self.frm_right_title,
                                                              text= '                          ',
                                                              font=font)

        #self.textInfo = PyText(self.frm_right_title,width=19,height=1)
        #self.textInfo.insert('insert', "Hello.....")
        self.labelTitle.grid(row=0, column=0, padx=1, pady=2, sticky="wesn")

    def create_frm_right_information(self):

        self.labelDeviceName1 = PyLabel(self.frm_right_information, text= 'device_name: ', font=font )
        self.entryDeviceName = tk.StringVar()
        self.entryDeviceName2 = PyEntry(self.frm_right_information,
                                                              textvariable=self.entryDeviceName,
                                                              width=23,
                                                              font=font)
        self.entryDeviceName.set('NA')

        self.labelSN1 = PyLabel(self.frm_right_information, text= 'Serial Number: ', font=font )
        self.labelSN2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelMCU1 = PyLabel(self.frm_right_information, text= 'FEP(MCU) version: ', font=font )
        self.labelMCU2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelDSP1 = PyLabel(self.frm_right_information, text= 'DSP version: ', font=font )
        self.labelDSP2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelDevice_version1 = PyLabel(self.frm_right_information, text= 'device_version: ', font=font )
        self.entryDevice_version = tk.StringVar()
        self.entryDevice_version2 = PyEntry(self.frm_right_information,
                                                              textvariable=self.entryDevice_version,
                                                              width=23,
                                                              font=font)
        self.entryDevice_version.set('NA')

        self.labelIP1 = PyLabel(self.frm_right_information, text= 'IP: ', font=font )
        self.entryIP = tk.StringVar()
        self.entryIP2 = PyEntry(self.frm_right_information,
                                                              textvariable=self.entryIP,
                                                              width=23,
                                                              font=font)
        self.entryIP.set('NA')

        self.labelDevice_wifi1 = PyLabel(self.frm_right_information, text= 'wifi_device: ', font=font )
        self.labelDevice_wifi2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelWifi_level1 = PyLabel(self.frm_right_information, text= 'wifi_level: ', font=font )
        self.labelWifi_level2 = PyLabel(self.frm_right_information, text= 'NA', font=font)


        self.labelBt_open1 = PyLabel(self.frm_right_information, text= 'bt_open: ', font=font )
        self.bt_open = tk.IntVar()
        self.CheckbtnBt_open2 = PyCheckbutton(self.frm_right_information,
                                              text="Enable always open",
                                              variable=self.bt_open,
                                              font=font)

        self.btnPair = PyButton(self.frm_right_information,
                                          text="Pair",
                                          font=font,
                                          width=6,
                                          state='active',
                                          command=self.__onBtnPair)

        self.labelBt_connectWay1 = PyLabel(self.frm_right_information, text= 'bt_connectWay: ', font=font )
        bt_reconnet = ["NA","Manual", "Automatic", "Disable",]#manual automatic none
        self.comboboxBt_reconnet = ttk.Combobox(self.frm_right_information,
                                                       width=15,
                                                       values=bt_reconnet)
        #self.MobileNumberChosen.current(0)
        self.comboboxBt_reconnet.set('NA')

        self.labelNum_btpaired1 = PyLabel(self.frm_right_information, text= 'bt_num_paired: ', font=font )
        self.labelNum_btpaired2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelDevice_btpaired1 = PyLabel(self.frm_right_information, text= 'bt_device_paired: ', font=font )
        self.labelDevice_btpaired2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelConnect_status1 = PyLabel(self.frm_right_information, text= 'bt_connect_status: ', font=font )
        self.labelConnect_status2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelVolume_default1 = PyLabel(self.frm_right_information, text= 'volume_default: ', font=font )
        self.labelVolume_default2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelVolume_max1 = PyLabel(self.frm_right_information, text= 'volume_max: ', font=font )
        self.labelVolume_max2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelVolume_current1 = PyLabel(self.frm_right_information, text= 'volume_current: ', font=font )
        self.labelVolume_current2 = PyLabel(self.frm_right_information, text= 'NA', font=font)

        self.labelBattery = PyLabel(self.frm_right_information, text= 'battery: ', font=font )
        self.labelBattery2 = PyLabel(self.frm_right_information, text= 'Percentage: NA\nHealthStatus: NA\nStatus: NA', font=font)

        self.labelTemp1 = PyLabel(self.frm_right_information, text= 'Temperature: ', font=font )
        self.labelTemp2 = PyLabel(self.frm_right_information, text= 'Amp1: NAC° Amp2: NAC°', font=font)

        self.labelSoundpos1 = PyLabel(self.frm_right_information, text= 'Sound Position: ', font=font )
        self.labelSoundpos2 = PyLabel(self.frm_right_information, text= 'NA', font=font)
        #Percentage: 66%, HealthStatus: good , Status: high
        #---------------------------------------------------------------

        self.labelDeviceName1.grid(row=0, column=0, padx=1, pady=2, sticky="e")
        self.entryDeviceName2.grid(row=0, column=1, padx=1, pady=2, sticky="w")

        self.labelMCU1.grid(row=1, column=0, padx=1, pady=2, sticky="e")
        self.labelMCU2.grid(row=1, column=1, padx=1, pady=2, sticky="w")

        self.labelDevice_version1.grid(row=3, column=0, padx=1, pady=2, sticky="e")
        self.entryDevice_version2.grid(row=3, column=1, padx=1, pady=2, sticky="w")

        self.labelIP1.grid(row=4, column=0, padx=1, pady=2, sticky="e")
        self.entryIP2.grid(row=4, column=1, padx=1, pady=2, sticky="w")

        self.labelBt_open1.grid(row=5, column=0, padx=1, pady=2, sticky="e")
        self.CheckbtnBt_open2.grid(row=5, column=1, padx=1, pady=2, sticky="w")

        self.labelBt_connectWay1.grid(row=7, column=0, padx=1, pady=2, sticky="e")
        self.comboboxBt_reconnet.grid(row=7, column=1, padx=1, pady=2, sticky="w")

        self.labelDevice_btpaired1.grid(row=8, column=0, padx=1, pady=2, sticky="e")
        self.labelDevice_btpaired2.grid(row=8, column=1, padx=1, pady=2, sticky="w")

        #self.labelDSP1.grid(row=2, column=0, padx=1, pady=2, sticky="e")
        #self.labelDSP2.grid(row=2, column=1, padx=1, pady=2, sticky="w")

        #self.labelSN1.grid(row=1, column=0, padx=1, pady=2, sticky="e")
        #self.labelSN2.grid(row=1, column=1, padx=1, pady=2, sticky="w")

        #self.labelDevice_wifi1.grid(row=6, column=0, padx=1, pady=2, sticky="e")
        #self.labelDevice_wifi2.grid(row=6, column=1, padx=1, pady=2, sticky="w")

        #self.labelWifi_level1.grid(row=7, column=0, padx=1, pady=2, sticky="e")
        #self.labelWifi_level2.grid(row=7, column=1, padx=1, pady=2, sticky="w")

        #self.btnPair.grid(row=9, column=1, padx=1, pady=2, sticky="w")

        #self.labelNum_btpaired1.grid(row=11, column=0, padx=1, pady=2, sticky="e")
        #self.labelNum_btpaired2.grid(row=11, column=1, padx=1, pady=2, sticky="w")

        #self.labelConnect_status1.grid(row=13, column=0, padx=1, pady=2, sticky="e")
        #self.labelConnect_status2.grid(row=13, column=1, padx=1, pady=2, sticky="w")

        #self.labelVolume_default1.grid(row=14, column=0, padx=1, pady=2, sticky="e")
        #self.labelVolume_default2.grid(row=14, column=1, padx=1, pady=2, sticky="w")

        #self.labelVolume_max1.grid(row=15, column=0, padx=1, pady=2, sticky="e")
        #self.labelVolume_max2.grid(row=15, column=1, padx=1, pady=2, sticky="w")

        #self.labelVolume_current1.grid(row=16, column=0, padx=1, pady=2, sticky="e")
        #self.labelVolume_current2.grid(row=16, column=1, padx=1, pady=2, sticky="w")

        #self.labelBattery.grid(row=17, column=0, padx=1, pady=2, sticky="e")
        #self.labelBattery2.grid(row=17, column=1, padx=1, pady=2, sticky="w")

        #self.labelTemp1.grid(row=18, column=0, padx=1, pady=2, sticky="e")
        #self.labelTemp2.grid(row=18, column=1, padx=1, pady=2, sticky="w")

        #self.labelSoundpos1.grid(row=19, column=0, padx=1, pady=2, sticky="e")
        #self.labelSoundpos2.grid(row=19, column=1, padx=1, pady=2, sticky="w")

    def create_frm_right_operation(self):

        self.btnRefreshInfo = PyButton(self.frm_right_operation,
                                          text="Refresh",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnRefreshInfo)

        self.btnEdit = PyButton(self.frm_right_operation,
                                          text="Edit",
                                          font=font,
                                          width=6,
                                          state='active',
                                          command=self.__onBtnEdit)

        self.btnUnlock = PyButton(self.frm_right_operation,
                                          text="Unlock",
                                          font=font,
                                          width=6,
                                          state='active',
                                          command=self.__onBtnUnlock)

        self.labelEmpty = PyLabel(self.frm_right_operation, text= ' '*33, font=font)

        self.btnReset = PyButton(self.frm_right_operation,
                                          text=" Factory Reset ",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnReset)

        self.btnRefreshInfo.grid(row=0, column=0, padx=1, pady=2, sticky="e")
        self.btnEdit.grid(row=0, column=1, padx=1, pady=2, sticky="wesn")
        self.btnUnlock.grid(row=0, column=2, padx=1, pady=2, sticky="e")
        self.labelEmpty.grid(row=0, column=3, padx=1, pady=2, sticky="e")
        self.btnReset.grid(row=0, column=4, padx=1, pady=2, sticky="e")

    def create_frm_right_page(self):
        self.btnBack = PyButton(self.frm_right_page,
                                          text=" BACK ",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnBack)

        self.labelEmpty = PyLabel(self.frm_right_page, text= ' '*34, font=font)

        self.btnWebpage = PyButton(self.frm_right_page,
                                          text="Go to WebPage",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnWebpage)

        self.btnAutoUpdate = PyButton(self.frm_right_page,
                                          text="OTA Auto update",
                                          font=font,
                                          state='active',
                                          command=self.__onBtnAutoUpdate)

        self.btnBack.grid(row=0, column=0, padx=1, pady=2, sticky="w")
        self.labelEmpty.grid(row=0, column=1, padx=1, pady=2, sticky="w")
        self.btnWebpage.grid(row=0, column=2, padx=1, pady=2, sticky="w")
        self.btnAutoUpdate.grid(row=0, column=3, padx=1, pady=2, sticky="w")

    '''
    def create_frm_right_savepath(self):
        self.frm_right_savepath_label = PyLabel(self.frm_right_savepath,
                                                  text=''+ " "*size_dict["clear_label_width"],
                                                  font=font)

        self.frm_right_savepath_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
    '''

    def create_frm_status(self):
        self.labelStatus = PyLabel(self.frm_status,
                                             text="Ready",
                                             font=font)
        self.labelStatus.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    #---------------------------------------------------------------------------------
    def __onBtnUnlock(self):
        _thread.start_new_thread(self.__Unlock, ())

    def __Unlock(self):
        status = str(self.GetAse('readinfo')[-1], 'utf-8')
        if 'Successful' in status:
            messagebox.showinfo('Unlock', 'Unlock Successfully!')
        else:
            messagebox.showinfo('Unlock', 'Unlock Failed!')

    def __onBtnInputIP(self):
        inputIP = self.inputIPStr.get()
        p = re.compile(r'(?:(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d|2[0-4]\d|25[0-5])')
        if p.match(inputIP):
            self.ip = inputIP
            self.__showRightFrm()
            self.inputIPStr.set('')
        else:
            messagebox.showerror('IP Error', 'Please input standard IP address!')
            self.inputIPStr.set('')

    def __onBtnAutoUpdate(self):
        #self.root.destroy()
        #self.frm_left.grid_forget()
        #self.frm_right.grid_forget()
        #self.btnAutoUpdate['state'] = 'disabled'
        FrameUpdateSet(self.root, self.title, self.icon, self.ip, self.modelName)

    def __onBtnWebpage(self):
        url = "http://{0}/index.fcgi".format(self.ip)
        try:
            threading.Timer(0, lambda: webbrowser.open(url) ).start()
        except Exception as e:
            logging.log(logging.DEBUG, e)

    def __onBtnPair(self):
        if self.btnPair['text'] == 'Pair':
            self.btnPair['text'] = 'Cancel'
            self.pair_url = 'http://'+self.ip+'/api/setData?path=bluetooth%3AexternalDiscoverable&roles=activate&value=%7B%22type%22%3A%22bool_%22%2C%22bool_%22%3Atrue%7D&'
            dev_status.get_url(self.pair_url)
        else:
            self.btnPair['text'] = 'Pair'
            self.pair_url = 'http://'+self.ip+'/api/setData?path=bluetooth%3AexternalDiscoverable&roles=activate&value=%7B%22type%22%3A%22bool_%22%2C%22bool_%22%3Afalse%7D&'
            dev_status.get_url(self.pair_url)

    def __onBtnReboot(self):
        self.GetAse('reboot')
        self.__onBtnBack()

    def __onBtnReset(self):
        self.reset_url = 'http://'+self.ip+'/api/setData?path=beo_LocalUI%3AfactoryResetRequest&roles=activate&value=%7B\"type\"%3A\"bool_\"%2C\"bool_\"%3Atrue%7D&'
        dev_status.get_url(self.reset_url)
        self.__onBtnBack()

    def __onBtnClose(self):
        self.root.destroy()#quit
        sleep(2)
        sys.exit()

    def __onBtnBack(self):
        self.infoPage = 0
        _thread.start_new_thread(deviceScan(self.infoPage, self.labelStatus, self.__listBoxDeviceName, messagebox).scan, ())
        #self.backFlag = 0
        self.frm_right.grid_forget()
        self.frm_left.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

        self.labelStatus['text'] = 'Device Scanning...'
        self.labelTitle['text'] = ' '
        self.entryDeviceName.set('NA')
        self.entryDevice_version.set('NA')
        self.labelMCU2['text'] = 'NA'
        self.entryIP.set('NA')
        self.bt_open.set('NA')
        self.labelDevice_btpaired2['text'] = 'NA'
        '''
        self.labelDevice_wifi2['text'] = 'NA'
        self.labelWifi_level2['text'] = 'NA'
        self.comboboxBt_reconnet.set('NA')
        self.labelVolume_default2['text'] = 'NA'
        self.labelVolume_max2['text'] = 'NA'
        self.labelConnect_status2['text'] = 'NA'
        self.labelVolume_current2['text'] = 'NA'
        self.labelBattery2['text'] = 'Percentage: NA\nHealthStatus: NA\nStatus: NA'
        self.labelTemp2['text']  = 'Amp1: NAC° Amp2: NAC°'
        self.labelSN2['text'] = 'NA'
        self.labelMCU2['text'] = 'NA'
        self.labelSoundpos2['text'] = 'NA'
        self.labelDSP2['text'] = 'NA'
        '''

    def __onBtnRefresh(self):
        _thread.start_new_thread(deviceScan(self.infoPage, self.labelStatus, self.__listBoxDeviceName, messagebox).scan, ())

    def __onBtnEdit(self):
        _thread.start_new_thread(self.Edit, ())

    def Edit(self):
        if self.btnEdit['text'] == 'Edit':
            self.btnEdit['text'] = 'Save'
            self.labelStatus['text'] = 'Please modify and then press "Save" button!'
            #self.__listBoxDeviceName['state'] = 'disabled'
            self.btnBack['state'] = 'disabled'
            self.btnReset['state'] = 'disabled'
            self.labelDeviceName1.grid(row=0, column=0, padx=1, pady=2, sticky="e")
            self.entryDeviceName2.grid(row=0, column=1, padx=1, pady=2, sticky="w")

        else:
            self.btnEdit['text'] = 'Edit'
            #-------
            if (self.ip != 'NA') and (self.entryDeviceName.get() != ''):
                if len(self.entryDeviceName.get())<=18:
                    self.change_name_url = 'http://'+self.ip+'/api/setData?path=settings%3A%2FdeviceName&roles=value&value=%7B\"type\"%3A\"string_\"%2C\"string_\"%3A\"'+self.entryDeviceName.get()+'\"%7D&'
                    dev_status.get_url(self.change_name_url)
            #-------
            if self.bt_open.get() == 1:
                open_enable = 'true'
            else:
                open_enable = 'false'
            self.bt_openset_url = 'http://'+self.ip+'/api/setData?path=settings%3A%2Fbluetooth%2FpairingAlwaysEnabled&roles=value&value=%7B\"type\"%3A\"bool_\"%2C\"bool_\"%3A'+open_enable+'%7D&'
            dev_status.get_url(self.bt_openset_url)
            #-------
            if self.comboboxBt_reconnet.get()== 'Manual':
                self.bt_reconnect_url = 'http://'+self.ip+'/api/setData?path=settings%3A%2Fbluetooth%2FautoConnect&roles=value&value=%7B\"type\"%3A\"bluetoothAutoConnectMode\"%2C\"bluetoothAutoConnectMode\"%3A\"manual\"%7D&'
            elif self.comboboxBt_reconnet.get()== 'Automatic':
                self.bt_reconnect_url = 'http://'+self.ip+'/api/setData?path=settings%3A%2Fbluetooth%2FautoConnect&roles=value&value=%7B\"type\"%3A\"bluetoothAutoConnectMode\"%2C\"bluetoothAutoConnectMode\"%3A\"automatic\"%7D&'
            else:
                self.bt_reconnect_url = 'http://'+self.ip+'/api/setData?path=settings%3A%2Fbluetooth%2FautoConnect&roles=value&value=%7B\"type\"%3A\"bluetoothAutoConnectMode\"%2C\"bluetoothAutoConnectMode\"%3A\"none\"%7D&'
            dev_status.get_url(self.bt_reconnect_url)
            self.labelStatus['text'] = 'Ready'
            #self.__listBoxDeviceName['state'] = 'normal'
            self.btnBack['state'] = 'normal'
            self.btnReset['state'] = 'normal'
            self.labelDeviceName1.grid_forget()
            self.entryDeviceName2.grid_forget()
            _thread.start_new_thread(self.refresh_static, ())

    def __showRightFrm(self):
            self.backFlag = 1 #change to right frame
            self.frm_left.grid_forget()
            self.frm_right.grid(row=0, column=1, padx=5, pady=5, sticky="wesn")

            self.infoPage = 1
            self.labelDeviceName1.grid_forget()
            self.entryDeviceName2.grid_forget()

            _thread.start_new_thread(self.refresh_static, ())

    def __onlistSelectBtnClick(self, event):
        try:
            s=self.__listBoxDeviceName.get(self.__listBoxDeviceName.curselection())
            a,selectDevice=s.split(">")

            self.deviceName = re.findall(u'(.+) \(', selectDevice)[0]
            self.ip = re.findall(u' \((.+)\)', selectDevice)[0]
            #self.device = re.findall(u'\)\[(.+)\]', selectDevice)[0]
            self.__showRightFrm()
            """
            if self.device == 'FS1':
                self.labelBattery.grid(row=14, column=0, padx=1, pady=2, sticky="e")
                self.labelBattery2.grid(row=14, column=1, padx=1, pady=2, sticky="w")
            elif self.device == 'CA16':
                self.labelBattery.grid_forget()
                self.labelBattery2.grid_forget()
            else:
                pass
            """
        except Exception as e:
            logging.log(logging.DEBUG, e)

    """
    ############################################################################################
    """
    def __onBtnRefreshInfo(self):
        self.btnRefreshInfo['state'] = 'disabled'
        _thread.start_new_thread(self.refresh_static, ())

    def refresh_static(self):
        try:
            for i in range(0,3):
                if self.infoPage == 0:
                    return
                self.labelStatus['text'] = 'Information Refreshing.'

                basicInfo = dev_status.status_static('basicInfo', self.ip)
                device_name = dev_status.status_static('device_name', self.ip)
                self.modelName = basicInfo['modelName']
                if self.infoPage == 0:
                    return

                self.entryDeviceName.set(device_name)
                self.labelTitle['text'] = device_name + '(' + self.modelName +'):'
                self.labelMCU2['text'] = basicInfo['appVersion']

                self.labelStatus['text'] = 'Information Refreshing..'
                self.entryDevice_version.set(dev_status.status_static('device_version', self.ip))
                self.entryIP.set(self.ip)

                self.labelStatus['text'] = 'Information Refreshing...'

                self.bt_open.set(dev_status.status_static('bt_open', self.ip))
                if self.bt_open.get() == 1:
                    self.btnPair.grid_forget()
                else:
                    self.btnPair.grid(row=6, column=1, padx=1, pady=2, sticky="w")

                self.comboboxBt_reconnet.set(dev_status.status_static('bt_connectWay', self.ip))

                self.labelVolume_default2['text'] = dev_status.status_static('volume_default', self.ip)
                self.labelVolume_max2['text'] = dev_status.status_static('volume_max', self.ip)

                bt_info = dev_status.status_static('bt', self.ip)
                #print(bt_info['rowsCount'])
                btDevices = ''
                for bt in bt_info['rows']:
                    if bt[2] != '':
                        btDevices = bt[0] + ' ['+ bt[1] + '] [' + bt[2]+']\n' + btDevices
                    else:
                        btDevices = bt[0] + ' ['+ bt[1] + '] ' +bt[2]+'\n' + btDevices

                self.labelDevice_btpaired2['text'] = btDevices

                #self.labelConnect_status2['text'] = device_connect_status
                '''
                if bt_info[0] != '0':
                    count = 0
                    line = ''
                    btDevices = ''
                    connect_flag = 0
                    for i in range(0, len(bt_info)):
                        s = bt_info[i]
                        if s != 0:#name mac status
                            if i == 0 :
                                self.labelNum_btpaired2['text'] = s
                            elif i == 1 + 3*count:#name
                                btDevice = '%s.%s'%(count+1,s)
                                name = s
                                btDevices = '%s %s%s\n'%(btDevices, btDevice,line)

                                #if i%2 == 0:
                                #    line = '\n'
                                #else:
                                #    line = ''

                            elif i == 2 + 3*count:#mac
                                mac = s
                            elif i == 3 + 3*count: #status
                                count += 1
                                if s == 'connected':
                                    device_connect_status = '%s\nconnected\n[%s]'%(name,mac)
                                    connect_flag = 1
                                elif connect_flag == 0:
                                    device_connect_status = ' '
                else:
                    self.labelNum_btpaired2['text'] = '0'
                    btDevices = ' '
                    device_connect_status = ' '
                self.labelDevice_btpaired2['text'] = btDevices
                self.labelConnect_status2['text'] = device_connect_status
                '''
        except Exception as e:
            logging.log(logging.DEBUG, e)
        self.labelStatus['text'] = 'Ready'
        self.btnRefreshInfo['state'] = 'normal'
        '''
        try:
            thread_refresh_static = threading.Timer(0, self.refresh_static)
            thread_refresh_static.daemon=True
            thread_refresh_static.start()
        except Exception as e:
            logging.log(logging.DEBUG, e)
        '''

    def refresh_dynamic(self):
        if self.infoStart == 1:
            if self.refresh_info == 1:
                try:
                    self.labelVolume_current2['text'] = dev_status.status_dynamic('volume_current', self.ip)

                    if self.device == 'FS1':
                        self.labelBattery2['text'] = 'Percentage: %s%%\nHealthStatus: %s\nStatus: %s'%(dev_status.status_dynamic('batteryPercentage', self.ip),dev_status.status_dynamic('batteryHealthStatus', self.ip),dev_status.status_dynamic('batteryStatus', self.ip))
                except:
                    pass
        try:
            thread_FreshDynamic = threading.Timer(0.2, self.refresh_dynamic)
            thread_FreshDynamic.setDaemon(True)
            thread_FreshDynamic.start()
        except Exception as e:
            logging.log(logging.DEBUG, e)

    def refresh_temperature(self):
        if self.infoStart == 1:
            if self.refresh_info == 1:
                temperature = str(self.GetAse('readtemp')[0], 'utf-8')
                try:
                    if "Temp" in temperature:
                        amp1 = re.findall(u'amp1=(.+)C \/ amp2', temperature)[0]
                        amp2 = re.findall(u'amp2=(.+)C', temperature)[0]
                        self.labelTemp2['text']  = 'Amp1: '+amp1+'C° Amp2: '+amp2+'C°'
                    else:
                        self.labelTemp2['text']  = 'Amp1: NAC° Amp2: NAC°'
                except:
                    pass
            else:
                self.labelTemp2['text']  = 'Amp1: NAC° Amp2: NAC°'
        try:
            thread_temperature = threading.Timer(0.3, self.refresh_temperature)
            thread_temperature.setDaemon(True)
            thread_temperature.start()
        except:
            pass

    def refresh_aseinfo(self):
        if self.infoStart == 1:
            if self.refresh_info == 1:
                ase_readinfo = self.GetAse('readinfo')
                print(ase_readinfo)
                try:
                    ase_sn = str(ase_readinfo[0],'utf-8')
                    if 'serial' in ase_sn:
                        self.labelSN2['text'] = re.findall(u'serial=(.+), wifi', ase_sn)[0]

                    ase_version = str(ase_readinfo[1],'utf-8')
                    if 'Ver' in ase_version:
                        FW = re.findall(u'FW v(.+) FW', ase_version)[0]
                        HW = re.findall(u'HW (.+) HW', ase_version)[0]
                        self.labelMCU2['text'] = FW+'('+HW+')'

                    ase_dspversion = str(ase_readinfo[1],'utf-8')
                    if 'DSP' in ase_dspversion:
                        self.labelDSP2['text'] = re.findall(u'DSP v(.+) DSP', ase_dspversion)[0]

                    if self.device == 'CA16':
                        #free Wall Corner
                        ase_soundpos = str(ase_readinfo[2],'utf-8')
                        if 'pos' in ase_soundpos:
                            SoundPos = re.findall(u'pos=(.+)', ase_soundpos)[0]
                            if SoundPos == '1':
                                self.labelSoundpos2['text'] = 'Free'
                            elif SoundPos == '2':
                                self.labelSoundpos2['text'] = 'Wall'
                            elif SoundPos == '3':
                                self.labelSoundpos2['text'] = 'Corner'
                            else:
                                self.labelSoundpos2['text'] = 'NA'
                    #print(ase_soundpos)
                except:
                    return
            else:
                self.labelSN2['text'] = 'NA'
                self.labelMCU2['text'] = 'NA'
                self.labelSoundpos2['text'] = 'NA'
                self.labelDSP2['text'] = 'NA'
        try:
            thread_aseinfo = threading.Timer(0.2, self.refresh_aseinfo)
            thread_aseinfo.setDaemon(True)
            thread_aseinfo.start()
        except:
            pass

    """Asetk_command
    ################################################################
    """
    def GetAse(self,info):
        pipe = ''
        #if self.root.winfo_exists()== 1:
        try:
            s=subprocess.Popen(r""+os.getcwd()+"\\src\\config\\thrift\\thrift2.exe "+self.ip+" 1 "+info,shell=True,stdout=subprocess.PIPE)
            pipe=s.stdout.readlines()
        except:
            return pipe
        return pipe


if __name__ == '__main__':
    mainFrame = MainFrame()
    mainFrame.mainLoop()
