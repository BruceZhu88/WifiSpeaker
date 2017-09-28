#-------------------------------------------------------------------------------
# Name:        FrameLogPrint
# Purpose:
#
# Author:      Bruce.Zhu
#
# Created:     05/09/2017
# Copyright:   (c) SQA 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from .PyTkinter import *
import tkinter as tk
import time

from src.common.logger_config import logger

class FrameLogPrint:

    def __init__(self, Root, title='', icon='', status=1):
        """"""
        self.title = title
        self.icon = icon
        self.root = Root
        self.top = tk.Toplevel(self.root)

        self.__firstLogIdx = 0
        self.__lastLogIdx = 0
        self.__lastSavedLogIdx = 0
        self.__autoSave = False
        self.__autoSavePath = None

        self.__textLog = None
        self.__autoSaveTimer = None

        self.__cacheCommand = []
        self.__cachePos = -1
        self.frm_right_print = None

        self.create_frm(status)
        self.__setupTop()

    def __setupTop(self):
        #self.top.protocol('WM_DELETE_WINDOW', lambda:0) #ignore close
        self.top.title(self.title)
        self.top.iconbitmap(self.icon)

        self.top.resizable(True, True)
        self.top.minsize(650, 400)
        self.top.configure(bg ='white')

        # center root
        screenWidth = self.top.winfo_screenwidth()
        screenHeight = self.top.winfo_screenheight()
        rootWidth = 650
        rootHeight = 400
        size = '%dx%d+%d+%d' % (rootWidth, rootHeight, (screenWidth - rootWidth)/2, (screenHeight - rootHeight)/2)
        self.top.geometry(size)
        self.top.attributes('-topmost', 1)

    def create_frm(self, status):
        self.frm_logPrint = tk.Frame(self.top)
        self.frm_status = tk.Frame(self.top, bg="#292929")
        self.frm_logPrint.pack(side='top', fill='both', expand='yes')
        self.frm_status.pack(side='bottom', fill='x')
        self.create_frm_logPrint()
        if status==1:
            self.create_frm_status()
        elif status==2:
            self.create_frm_status2()            

    def create_frm_logPrint(self):
        self.frm_right_print = PyScrolledText(self.frm_logPrint,
                                             font=("Monaco", 9),
                                             relief='flat')
        self.frm_right_print.tag_config("green", foreground="#228B22")
        self.frm_right_print.pack(fill='both', expand='yes')

    def create_frm_status(self):
        self.labelStartTime = PyLabel(self.frm_status, text='Start Time: ', font=("Monaco", 9))
        self.labelShowStartTime = PyLabel(self.frm_status, text='', font=("Monaco", 9))
        self.labelElapsedTime = PyLabel(self.frm_status, text='Elapsed Time: ', font=("Monaco", 9))
        self.labelShowElapsedTime = PyLabel(self.frm_status, text='', font=("Monaco", 9))

        self.labelRuntimes = PyLabel(self.frm_status, text='Total Times: ', font=("Monaco", 9))
        self.labelShowRuntimes = PyLabel(self.frm_status, text='', font=("Monaco", 9))
        self.labelNetworkError = PyLabel(self.frm_status, text='NetworkError: ', font=("Monaco", 9))
        self.labelShowNetworkError = PyLabel(self.frm_status, text='0', font=("Monaco", 9))
        self.labelPass = PyLabel(self.frm_status, text='Pass: ', font=("Monaco", 9))
        self.labelShowPass = PyLabel(self.frm_status, text='0/0(Upgrade) 0/0(Downgrade)', font=("Monaco", 9))

        self.labelStartTime.grid(row=0, column=0, padx=1, pady=1, sticky="w")
        self.labelShowStartTime.grid(row=0, column=1, padx=1, pady=1, sticky="w")
        self.labelElapsedTime.grid(row=0, column=2, padx=1, pady=1, sticky="w")
        self.labelShowElapsedTime.grid(row=0, column=3, padx=1, pady=1, sticky="w")

        self.labelRuntimes.grid(row=1, column=0, padx=1, pady=1, sticky="w")
        self.labelShowRuntimes.grid(row=1, column=1, padx=1, pady=1, sticky="w")
        self.labelNetworkError.grid(row=1, column=2, padx=1, pady=1, sticky="w")
        self.labelShowNetworkError.grid(row=1, column=3, padx=1, pady=1, sticky="w")
        self.labelPass.grid(row=1, column=4, sticky="w")
        self.labelShowPass.grid(row=1, column=5, sticky="w")

    def create_frm_status2(self):
        self.labelTotalTimes = PyLabel(self.frm_status, text='Total Times: ', font=("Monaco", 9))
        self.labelShowTotalTimes = PyLabel(self.frm_status, text='', font=("Monaco", 9))
        self.labelDHCP = PyLabel(self.frm_status, text='DHCP: ', font=("Monaco", 9))
        self.labelShowDHCP = PyLabel(self.frm_status, text='', font=("Monaco", 9))        
        self.labelSuccesTimes = PyLabel(self.frm_status, text='Success Times: ', font=("Monaco", 9))
        self.labelShowSuccesTimes = PyLabel(self.frm_status, text='', font=("Monaco", 9))
        
        self.labelTotalTimes.grid(row=0, column=0, padx=1, pady=1, sticky="w")
        self.labelShowTotalTimes.grid(row=0, column=1, padx=1, pady=1, sticky="w")
        self.labelDHCP.grid(row=0, column=2, padx=1, pady=1, sticky="w")
        self.labelShowDHCP.grid(row=0, column=3, padx=1, pady=1, sticky="w")
        self.labelSuccesTimes.grid(row=1, column=0, padx=1, pady=1, sticky="w")
        self.labelShowSuccesTimes.grid(row=1, column=1, padx=1, pady=1, sticky="w")
        
    def __onBtnExit(self):
        self.top.destroy()

    def mainLoop(self):
        #self.addLog('hah','')
        self.top.mainloop()

    def addLog(self, log, tag):
        logger.info(log)
        if log[-1] != '\n':
            log = log + '\n'

        timeStr = time.strftime('%H:%M:%S ', time.localtime(time.time()))

        self.frm_right_print.configure(state = 'normal')
        self.frm_right_print.insert('end', timeStr + tag + ' ' + log, 'log{0}'.format(self.__lastLogIdx))

        self.__lastLogIdx = self.__lastLogIdx + 1

        if self.__lastLogIdx - self.__firstLogIdx > 1000:
            firstTage = 'log{0}'.format(self.__firstLogIdx)
            firstTageIndex = self.frm_right_print.tag_ranges(firstTage)
            self.frm_right_print.delete(firstTageIndex[0], firstTageIndex[1])
            self.frm_right_print.tag_delete(firstTage)
            self.__firstLogIdx = self.__firstLogIdx + 1

        self.frm_right_print.see('end')

        #if self.__lastLogIdx - self.__lastSavedLogIdx > 100:
        #    self.__saveLog()

        self.frm_right_print.configure(state = 'disabled')

    def __onClearprintBtnClick(self):
        self.__saveLog()

        self.frm_right_print.configure(state = NORMAL)

        firstTage = 'log{0}'.format(self.__firstLogIdx)
        firstTageIndex = self.frm_right_print.tag_ranges(firstTage)
        lastTage = 'log{0}'.format(self.__lastLogIdx - 1)
        lastTageIndex = self.frm_right_print.tag_ranges(lastTage)

        #if not use try, when text is empty, it will report error
        try:
            self.frm_right_print.delete(firstTageIndex[0], lastTageIndex[1])

            while self.__lastLogIdx > self.__firstLogIdx:
                self.frm_right_print.tag_delete(firstTage)
                self.__firstLogIdx = self.__firstLogIdx + 1
                firstTage = 'log{0}'.format(self.__firstLogIdx)
        except:
            pass
        self.frm_right_print.see(END)
        self.frm_right_print.configure(state = DISABLED)

if __name__ == "__main__":
    frame = FrameLogPrint(tk.Tk())
    frame.mainLoop()
