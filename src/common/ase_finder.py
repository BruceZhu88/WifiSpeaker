import select
import socket
import logging
import sys
try:
    from . import pybonjour
except Exception as e:
    logging.log(logging.INFO, 'ERROR: Please install pybonjour module' + e)
    sys.exit(-1)

class deviceScan:

    def __init__(self, infoPage, labelStatus, listBoxDeviceName, messagebox):
        self.QUERY_TYPE = '_beo_settings._tcp'
        self.DNSSD_QUERY_TIMEOUT = 5
        self.queried = []
        self.resolved = []
        self.asetkNameReq = ''
        self.devName = ''
        self.friendlyName = ''
        self.ipaddr = ''
        self.times_scan = 1
        self.infoPage = infoPage
        self.labelStatus = labelStatus
        self.listBoxDeviceName = listBoxDeviceName
        self.messagebox = messagebox

    def resolve_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname, hosttarget, port, txtRecord):
        if self.infoPage == 1:
            return
        self.labelStatus['text'] = ' '
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
        record = txtRecord.split('=')
        if record[0].find('DEVICE_TYPE') >= 0:
            self.devName = record[1]
        else:
            self.devName = 'Unknown'
        self.friendlyName = fullname.split('.')[0].replace('\\032', ' ')
        self.ipaddr = socket.gethostbyname(hosttarget)
        if self.asetkNameReq == '' or self.friendlyName.find(self.asetkNameReq) >= 0:
            self.labelStatus['text'] = 'Device Scanning...'
            self.listBoxDeviceName.insert('end', '<{0}>{1} ({2})'.format(self.times_scan, self.friendlyName, self.ipaddr))
            self.times_scan += 1

    def browse_callback(self, sdRef, flags, interfaceIndex, errorCode, serviceName, regtype, replyDomain):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
        if not flags & pybonjour.kDNSServiceFlagsAdd:
            return
        resolve_sdRef = pybonjour.DNSServiceResolve(0, interfaceIndex, serviceName, regtype, replyDomain, self.resolve_callback)
        try:
            try:
                while not self.resolved:
                    ready = select.select([resolve_sdRef], [], [], self.DNSSD_QUERY_TIMEOUT)
                    if resolve_sdRef not in ready[0]:
                        break
                    pybonjour.DNSServiceProcessResult(resolve_sdRef)
                else:
                    self.resolved.pop()

            except Exception as e:
                logging.log(logging.DEBUG, e)

        finally:
            resolve_sdRef.close()

    def scan(self):
        self.listBoxDeviceName.delete(0, 'end')
        self.times_scan = 1
        try:
            browse_sdRef = pybonjour.DNSServiceBrowse(regtype=self.QUERY_TYPE, callBack=self.browse_callback)
        except Exception as e:
            logging.log(logging.DEBUG, e)
            self.messagebox.showinfo('Warning', "You didn't install bonjour or start server!")
            sys.exit()

        try:
            try:
                ready = select.select([browse_sdRef], [], [])
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
            except Exception as e:
                logging.log(logging.DEBUG, e)
                sys.exit(-1)

        finally:
            browse_sdRef.close()
            self.labelStatus['text'] = 'Ready'


if __name__ == '__main__':
    deviceScan = deviceScan()
    import threading
    threads = []
    main = threading.Thread(target=deviceScan.scan())
    threads.append(main)