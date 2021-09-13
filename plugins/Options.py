# coding:utf-8
import sys 
sys.path.append("..")
from Scanning.threadpoolscan import *
from plugins.porttoport import *


weishouquan = '837,2181,2375,5900,5984,6379,8834,8080,9200,11211,12345,27017,50070,50095'
toprce = '22,23,445,389,3389,80,443,4505,4506,8080,7001,3306,1433,1521,6379,27017,2375,5900,5432,4899'
def readfile(file):
    iplist=set()
    try:
        f = open(file,'r')
        for i in f:
            #print (i.strip())
            iplist.add(i.strip())
        f.close()
        return iplist
    except:
        print ('File read failed!')
        exit()



def options():
    if len(sys.argv)<4:
        print('USAGE:Please start scanning with Xscan.py ip.txt all 50 (timeout 默认0.1)')
        return
    try:
        timeout = float(sys.argv[4])

    except:
        timeout = 0.1

    if sys.argv[2] == 'all':
        ports = [i for i in range(65536)]
    elif sys.argv[2] == 'u':
        ports = weishouquan
    elif sys.argv[2] == 'w':
        ports = toprce
    else:
        ports = lrange(sys.argv[2])
        # print(ports)


    threads = sys.argv[3]
    hosts = readfile(sys.argv[1])

    scan=Scan()
    
    scan.threadstart(hosts,ports,threads,timeout)



    
    

if __name__ == '__main__':

    # port=[i for i in range(10000)]
    # ip = ['127.0.0.1']
    # options(50,ip,port,0.01
    # print(len(sys.argv))
    options()
