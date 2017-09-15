import threading
from src.ui import MainFrame
from src.common.logger import Logger

if __name__ == '__main__':
    log_conf = Logger.init_logger('project.log')
    mainFrame = MainFrame(log_conf['logfile'])
    threads = []
    main = threading.Thread(target=mainFrame.mainLoop())
    threads.append(main)
    '''
    mainFrame.infoStart = 0
    mainFrame.refresh_info = 0
    mainFrame.refresh_deviceList = 0
    time.sleep(3.3)#Wait all thread and progress to be finished
    sys.exit()#In case the progress can't be killed after UI closed by user
    '''
