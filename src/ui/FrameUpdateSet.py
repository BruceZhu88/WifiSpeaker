#-------------------------------------------------------------------------------
# Name:        FrameUpdateSet
# Purpose:
#
# Author:      Bruce.Zhu
#
# Created:     10/09/2017
# Copyright:   (c) SQA 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from .PyTkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import configparser
import time
import sys
import _thread
from src.common.aseUpdate import aseUpdate
from src.common.logger_config import logger
from .FrameLogPrint import FrameLogPrint

class FrameUpdateSet:

    def __init__(self, Root, title='', icon='', ip='', modelName=''):
        """"""
        try:
            conf = configparser.ConfigParser()
            conf.read('.\\aseUpdate.ini')
            #parent_path = os.path.realpath(os.path.join(os.getcwd(), ".."))
            self.low_version_path = conf.get("Firmware", "low_version_path")
            self.high_version_path = conf.get("Firmware", "high_version_path")
            self.low_version = conf.get("Firmware", "low_version").replace(' ', '')
            self.high_version = conf.get("Firmware", "high_version").replace(' ', '')
            self.cycle = conf.getint("Running_times", "times")
        except Exception as e:
            logger.debug(e)
            sys.exit()

        self.title = title
        self.icon = icon
        self.root = Root
        self.top = tk.Toplevel(self.root)

        self.create_frm()
        self.__setupTop()

        self.ip = ip
        self.modelName = modelName
        self.__Select_High_Path = ''
        self.__Select_Low_Path = ''

    def __setupTop(self):
        #self.top.protocol('WM_DELETE_WINDOW', lambda:0) #ignore close
        self.top.title(self.title + "--Settings for update")
        self.top.iconbitmap(self.icon)

        self.top.resizable(False, False)
        #self.top.minsize(600, 400)
        self.top.configure(bg = "#292929")

        # center root
        screenWidth = self.top.winfo_screenwidth()
        screenHeight = self.top.winfo_screenheight()
        rootWidth = 500
        rootHeight = 200
        size = '%dx%d+%d+%d' % (rootWidth, rootHeight, (screenWidth - rootWidth)/2, (screenHeight - rootHeight)/2)
        self.top.geometry(size)
        #self.top.attributes('-topmost', 1)

    def create_frm(self):
        self.frm_settings = tk.Frame(self.top, bg="#292929")
        self.frm_operation = tk.Frame(self.top, bg="#292929")
        self.frm_settings.pack(side='top')
        self.frm_operation.pack(side='bottom')
        self.create_frm_UpdateSet()
        self.create_frm_operation()

    def create_frm_UpdateSet(self):
        self.lableRuntimes = PyLabel(self.frm_settings, font=("Monaco", 9), text="Run Times: ")
        self.Runtimes = tk.StringVar()
        self.entryRuntimes = PyEntry(self.frm_settings, textvariable=self.Runtimes, font=("Monaco", 9))

        self.lableLowVersion = PyLabel(self.frm_settings, font=("Monaco", 9), text="Low Version: ")
        self.LowVersion = tk.StringVar()
        self.entryLowVersion = PyEntry(self.frm_settings, textvariable=self.LowVersion, font=("Monaco", 9))

        self.lableLowVersionPath = PyLabel(self.frm_settings, font=("Monaco", 9), text="low_version_path: ")
        self.LowVersionPath = tk.StringVar()
        self.entryLowVersionPath = PyEntry(self.frm_settings, textvariable=self.LowVersionPath, font=("Monaco", 9), width=40)
        self.btnLowPath = PyButton(self.frm_settings, font=("Monaco", 7), text="...", command=self.__onBtnLowPath)

        self.lableHighVersion = PyLabel(self.frm_settings, font=("Monaco", 9), text="HighVersion")
        self.HighVersion = tk.StringVar()
        self.entryHighVersion = PyEntry(self.frm_settings, textvariable=self.HighVersion, font=("Monaco", 9))

        self.lableHighVersionPath = PyLabel(self.frm_settings, font=("Monaco", 9), text="high_version_path: ")
        self.HighVersionPath = tk.StringVar()
        self.entryHighVersionPath = PyEntry(self.frm_settings, textvariable=self.HighVersionPath, font=("Monaco", 9), width=40)
        self.btnHighPath = PyButton(self.frm_settings, font=("Monaco", 7), text="...", command=self.__onBtnHighPath)

        self.lableRuntimes.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entryRuntimes.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.lableLowVersion.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entryLowVersion.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.lableLowVersionPath.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.entryLowVersionPath.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.btnLowPath.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.lableHighVersion.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.entryHighVersion.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.lableHighVersionPath.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.entryHighVersionPath.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.btnHighPath.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        self.Runtimes.set(self.cycle)
        self.LowVersionPath.set(self.low_version_path)
        self.HighVersionPath.set(self.high_version_path )
        self.LowVersion.set(self.low_version)
        self.HighVersion.set(self.high_version)

    def create_frm_operation(self):
        PyButton(self.frm_operation, font=("Monaco", 9), text="OK", width=12, command=self.__onBtnOK).pack(side='left')
        PyButton(self.frm_operation, font=("Monaco", 9), text="Cancle", width=12, command=self.__onBtnCancle).pack(side='right')

    def __onBtnLowPath(self):
        self.__Select_Low_Path = askopenfilename(title = 'Select low version path',
                                                filetypes = [('All files', '*.*')])
        self.LowVersionPath.set(self.__Select_Low_Path)

    def __onBtnHighPath(self):
        self.__Select_High_Path = askopenfilename(title = 'Select high version path',
                                                filetypes = [('All files', '*.*')])
        self.HighVersionPath.set(self.__Select_High_Path)

    def __onBtnCancle(self):
        self.top.destroy()

    def __onBtnOK(self):
        if (self.Runtimes.get()=='') or (self.LowVersionPath.get()=='') or \
            (self.HighVersionPath.get()=='') or (self.LowVersion.get()=='') or (self.HighVersion.get()==''):
            return

        conf = configparser.ConfigParser()
        try:
            path = './src/config/aseUpdate.ini'
            conf.read(path)
            conf.set("Running_times", "times", self.Runtimes.get())
            conf.set("Firmware", "low_version_path", self.LowVersionPath.get())
            conf.set("Firmware", "high_version_path", self.HighVersionPath.get())
            conf.set("Firmware", "low_version", self.LowVersion.get())
            conf.set("Firmware", "high_version", self.HighVersion.get())
            conf.write(open(path,"w"))
        except Exception as e:
            logger.debug('Error: {0}'.format(e))
            sys.exit()
        self.top.destroy()
        title = self.title + "--Auto update OTA for " + self.modelName
        framelogPrint = FrameLogPrint(self.root, title, self.icon, 1)
        _thread.start_new_thread(self.autoUpdate, (framelogPrint,))

    def autoUpdate(self, framelogPrint):
        update = aseUpdate(self.ip, self.modelName, framelogPrint)
        update.startOTA()

    def mainLoop(self):
        self.top.mainloop()

if __name__ == '__main__':
    frame = FrameUpdateSet(tk.Tk())
    frame.mainLoop()
