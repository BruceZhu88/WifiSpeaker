# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        checkUpdates
# Purpose:
#
# Author:      Bruce Zhu
#
# Created:     23/08/2017
# Copyright:   (c) SQA 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import urllib.request
import configparser
import zipfile
from src.common.logger_config import logger

class checkUpdates:

    def __init__(self):
        pass

    def downLoadFromURL(self, url, dest_dir):
        try:
            urllib.request.urlretrieve(url , dest_dir)
            return True
        except Exception as e:
            logger.debug('Error when downloading: {0}'.format(e))
            return False

    def getVer(self, verFile):
        downVer = ''
        conf = configparser.ConfigParser()
        try:
            conf.read(verFile)
            downVer = conf.get("version", "app")
        except Exception as e:
            logger.debug('Error: {0}'.format(e))
        return downVer

    def splitVer(self, s):
        ver = s.split('.')
        return ver

    def compareVer(self, downVer, currentVer):
        downVersions = self.splitVer(downVer)
        currentVersions = self.splitVer(currentVer)
        for i in range(0, len(currentVersions)):
            if int(downVersions[i]) > int(currentVersions[i]):
                return True
        return False

    def unzip_dir(self, zipfilename, unzipdirname):
        fullzipfilename = os.path.abspath(zipfilename)
        fullunzipdirname = os.path.abspath(unzipdirname)
        logger.debug("Start to unzip file %s to folder %s ..."% (zipfilename, unzipdirname) )
        #Check input ...
        if not os.path.exists(fullzipfilename):
            logger.debug("Dir/File %s is not exist, Press any key to quit..."% fullzipfilename  )
            inputStr = input()
            return
        if not os.path.exists(fullunzipdirname):
            os.mkdir(fullunzipdirname)
        else:
            if os.path.isfile(fullunzipdirname):
                logger.debug("File %s is exist, are you sure to delet it first ? [Y/N]"% fullunzipdirname)
                while 1:
                    inputStr = input()
                    if inputStr == "N" or inputStr == "n":
                        return
                    else:
                        if inputStr == "Y" or inputStr == "y":
                            os.remove(fullunzipdirname)
                            logger.debug("Continue to unzip files ...")
                            break
        #Start extract files ...
        #print(fullzipfilename)
        try:
            zipfiles=zipfile.ZipFile(fullzipfilename,'r')
            zipfiles.extractall(unzipdirname)
            zipfiles.close()
            logger.debug("Unzip finished!")
            logger.debug("Unzip file succeed!")
        except Exception as e:
            logger.debug(e)


if __name__ == '__main__':
    dest_dir = './downVer.ini'
    checkUpdates = checkUpdates()
    #checkUpdates.downLoadFromURL('http://sw.tymphany.com/fwupdate/sqa/tool/version.ini', dest_dir)
    #downVer = checkUpdates.getVer(dest_dir)
    #checkUpdates.compareVer(downVer, '1.1.0')
    checkUpdates.unzip_dir('PowerCycle.zip', 'PowerCycle')
