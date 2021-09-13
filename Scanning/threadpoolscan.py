# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor, wait
import socket,sys
sys.path.append("..")
from plugins.Showprocess import *
from plugins.printmsg import *
from plugins.banner import *
from plugins.color import color
import re
PROBE = {'GET / HTTP/1.0\r\n\r\n'}

class Scan():

    def start(self,show,ip,port):

        show.show_process()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, int(port)))
            if result == 0:

                try:
                    for i in PROBE:
                        sock.sendall(i.encode())
                        response = sock.recv(256)
                        sock.close()
                        if response:
                            regex(ip,port,response)
                except:
                    if get_server(port):
                        banner = get_server(port)
                        printYellow('ip:{} port:{} banner:{} '.format(ip,port,banner))
                    else:
                        printYellow('ip:{} port:{}'.format(ip,port))
            sock.close()
        except:
            pass

    def threadstart(self, hosts, ports, thread_num,timeout):
        
        show = ShowProcess(hosts,ports)
        show.show_process()
        socket.setdefaulttimeout(timeout)
        executor = ThreadPoolExecutor(max_workers=int(thread_num))
        for ip in hosts:
            t = [executor.submit(self.start, show,ip,n)for n in ports]
            if wait(t,return_when='ALL_COMPLETED'):
                pass
        printYellow('Done')

if __name__ == '__main__':
    ports=[i for i in range(65535)]
    hosts = ['127.0.0.1']
    ip = '10.243.75.41'
    port = ['445']
    Scan=Scan()
    show = ShowProcess(hosts,ports)
    Scan.start(show,ip,port)
