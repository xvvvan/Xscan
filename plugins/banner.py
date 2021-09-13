#coding:utf-8
import re,sys
sys.path.append("..")
from plugins.printmsg import *
from plugins.gettitle import *
from plugins.writeresult import *
from plugins.color import *
SIGNS = (
    # 协议 | 版本 | 关键字
    b'SMB|SMB|^\0\0\0.\xffSMBr\0\0\0\0.*',
    b'SMB|SMB|^\x83\x00\x00\x01\x8f',
    b"Xmpp|Xmpp|^\<\?xml version='1.0'\?\>",
    b'Netbios|Netbios|^\x79\x08.*BROWSE',
    b'Netbios|Netbios|^\x79\x08.\x00\x00\x00\x00',
    b'Netbios|Netbios|^\x05\x00\x0d\x03',
    b'Netbios|Netbios|^\x82\x00\x00\x00',
    b'Netbios|Netbios|\x83\x00\x00\x01\x8f',
    b'backdoor|backdoor|^500 Not Loged in',
    b'backdoor|backdoor|GET: command',
    b'backdoor|backdoor|sh: GET:',
    b'bachdoor|bachdoor|[a-z]*sh: .* command not found',
    b'backdoor|backdoor|^bash[$#]',
    b'backdoor|backdoor|^sh[$#]',
    b'backdoor|backdoor|^Microsoft Windows',
    b'DB2|DB2|.*SQLDB2RA',
    b'Finger|Finger|^\r\n	Line	  User',
    b'Finger|Finger|Line	 User',
    b'Finger|Finger|Login name: ',
    b'Finger|Finger|Login.*Name.*TTY.*Idle',
    b'Finger|Finger|^No one logged on',
    b'Finger|Finger|^\r\nWelcome',
    b'Finger|Finger|^finger:',
    b'Finger|Finger|^must provide username',
    b'Finger|Finger|finger: GET: ',
    b'FTP|FTP|^220'
    b'FTP|FTP|^220.*\n331',
    b'FTP|FTP|^220.*\n530',
    b'FTP|FTP|^220.*FTP',
    b'FTP|FTP|^220 .* Microsoft .* FTP',
    b'FTP|FTP|^220 Inactivity timer',
    b'FTP|FTP|^220 .* UserGate',
    b'FTP|FTP|^220.*FileZilla Server',
    b'LDAP|LDAP|^\x30\x0c\x02\x01\x01\x61',
    b'LDAP|LDAP|^\x30\x32\x02\x01',
    b'LDAP|LDAP|^\x30\x33\x02\x01',
    b'LDAP|LDAP|^\x30\x38\x02\x01',
    b'LDAP|LDAP|^\x30\x84',
    b'LDAP|LDAP|^\x30\x45',
    b'RDP|RDP|^\x00\x01\x00.*?\r\n\r\n$',
    b'RDP|RDP|^\x03\x00\x00\x0b',
    b'RDP|RDP|^\x03\x00\x00\x11',
    b'RDP|RDP|^\x03\0\0\x0b\x06\xd0\0\0\x12.\0$',
    b'RDP|RDP|^\x03\0\0\x17\x08\x02\0\0Z~\0\x0b\x05\x05@\x06\0\x08\x91J\0\x02X$',
    b'RDP|RDP|^\x03\0\0\x11\x08\x02..}\x08\x03\0\0\xdf\x14\x01\x01$',
    b'RDP|RDP|^\x03\0\0\x0b\x06\xd0\0\0\x03.\0$',
    b'RDP|RDP|^\x03\0\0\x0b\x06\xd0\0\0\0\0\0',
    b'RDP|RDP|^\x03\0\0\x0e\t\xd0\0\0\0[\x02\xa1]\0\xc0\x01\n$',
    b'RDP|RDP|^\x03\0\0\x0b\x06\xd0\0\x004\x12\0',
    b'RDP-Proxy|RDP-Proxy|^nmproxy: Procotol byte is not 8\n$',
    b'Msrpc|Msrpc|^\x05\x00\x0d\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00',
    b'Msrpc|Msrpc|\x05\0\r\x03\x10\0\0\0\x18\0\0\0....\x04\0\x01\x05\0\0\0\0$',
    b'Mssql|Mssql|^\x05\x6e\x00',
    b'Mssql|Mssql|^\x04\x01',
    b'Mssql|Mssql|;MSSQLSERVER;',
    b'MySQL|MySQL|mysql_native_password',
    b'MySQL|MySQL|^\x19\x00\x00\x00\x0a',
    b'MySQL|MySQL|^\x2c\x00\x00\x00\x0a',
    b'MySQL|MySQL|hhost \'',
    b'MySQL|MySQL|khost \'',
    b'MySQL|MySQL|mysqladmin',
    b'MySQL|MySQL|whost \'',
    b'MySQL|MySQL|^[.*]\x00\x00\x00\n.*?\x00',
    b'MySQL|MySQL|this MySQL server',
    b'MySQL|MySQL|MariaDB server',
    b'MySQL|MySQL|\x00\x00\x00\xffj\x04Host',
    b'db2jds|db2jds|^N\x00',
    b'Nagiosd|Nagiosd|Sorry, you \(.*are not among the allowed hosts...',
    b'Nessus|Nessus|< NTP 1.2 >\x0aUser:',
    b'oracle-tns-listener|\(ERROR_STACK=\(ERROR=\(CODE=',
    b'oracle-tns-listener|\(ADDRESS=\(PROTOCOL=',
    b'oracle-dbSNMP|^\x00\x0c\x00\x00\x04\x00\x00\x00\x00',
    b'oracle-https|^220- ora',
    b'RMI|RMI|\x00\x00\x00\x76\x49\x6e\x76\x61',
    b'RMI|RMI|^\x4e\x00\x09',
    b'PostgreSQL|PostgreSQL|Invalid packet length',
    b'PostgreSQL|PostgreSQL|^EFATAL',
    b'rpc-nfs|rpc-nfs|^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00',
    b'RPC|RPC|\x01\x86\xa0',
    b'RPC|RPC|\x03\x9b\x65\x42\x00\x00\x00\x01',
    b'RPC|RPC|^\x80\x00\x00',
    b'Rsync|Rsync|^@RSYNCD:',
    b'Rsync|Rsync|@RSYNCD:',
    b'smux|smux|^\x41\x01\x02\x00',
    b'snmp-public|snmp-public|\x70\x75\x62\x6c\x69\x63\xa2',
    b'SNMP|SNMP|\x41\x01\x02',
    b'Socks|Socks|^\x05[\x00-\x08]\x00',
    b'SSL|SSL|^..\x04\0.\0\x02',
    b'SSL|SSL|^\x16\x03\x01..\x02...\x03\x01',
    b'SSL|SSL|^\x16\x03\0..\x02...\x03\0',
    b'SSL|SSL|SSL.*GET_CLIENT_HELLO',
    b'SSL|SSL|^-ERR .*tls_start_servertls',
    b'SSL|SSL|^\x16\x03\0\0J\x02\0\0F\x03\0',
    b'SSL|SSL|^\x16\x03\0..\x02\0\0F\x03\0',
    b'SSL|SSL|^\x15\x03\0\0\x02\x02\.*',
    b'SSL|SSL|^\x16\x03\x01..\x02...\x03\x01',
    b'SSL|SSL|^\x16\x03\0..\x02...\x03\0',
    b'Sybase|Sybase|^\x04\x01\x00',
    b'Telnet|Telnet|Telnet',
    b'Telnet|Telnet|^\xff[\xfa-\xff]',
    b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
    b'Rlogin|Rlogin|login: ',
    b'Rlogin|Rlogin|rlogind: ',
    b'Rlogin|Rlogin|^\x01\x50\x65\x72\x6d\x69\x73\x73\x69\x6f\x6e\x20\x64\x65\x6e\x69\x65\x64\x2e\x0a',
    b'TFTP|TFTP|^\x00[\x03\x05]\x00',
    b'UUCP|UUCP|^login: password: ',
    b'VNC|VNC|^RFB',
    b'IMAP|IMAP|^\* OK.*?IMAP',
    b'POP|POP|^\+OK.*?',
    b'SMTP|SMTP|^220.*?SMTP',
    b'Kangle|Kangle|HTTP.*kangle',
    b'SMTP|SMTP|^554 SMTP',
    b'FTP|FTP|^220-',
    b'FTP|FTP|^220.*?FTP',
    b'FTP|FTP|^220.*?FileZilla',
    b'SSH|SSH|^SSH-',
    b'SSH|SSH|connection refused by remote host.',
    b'RTSP|RTSP|^RTSP/',
    b'SIP|SIP|^SIP/',
    b'NNTP|NNTP|^200 NNTP',
    b'SCCP|SCCP|^\x01\x00\x00\x00$',
    b'Webmin|Webmin|.*MiniServ',
    b'Webmin|Webmin|^0\.0\.0\.0:.*:[0-9]',
    b'websphere-javaw|websphere-javaw|^\x15\x00\x00\x00\x02\x02\x0a',
    b'Mongodb|Mongodb|MongoDB',
    b'Squid|Squid|X-Squid-Error',
    b'Mssql|Mssql|MSSQLSERVER',
    b'Vmware|Vmware|VMware',
    b'ISCSI|ISCSI|\x00\x02\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    b'Redis|Redis|^-ERR unknown command',
    b'Redis|Redis|^-ERR wrong number of arguments',
    b'Redis|Redis|^-DENIED Redis is running',
    b'MemCache|MemCache|^ERROR\r\n',
    b'WebSocket|WebSocket|Server: WebSocket',
    b'SVN|SVN|^\( success \( 2 2 \( \) \( edit-pipeline svndiff1',
    b'Dubbo|Dubbo|^Unsupported command',
    b'HTTP|Elasticsearch|cluster_name.*elasticsearch',
    b'RabbitMQ|RabbitMQ|^AMQP\x00\x00\t\x01',
    b'Pyspider|Pyspider|HTTP.*Dashboard - pyspider',
    b'HTTPS|HTTPS|Instead use the HTTPS scheme to access',
    b'HTTPS|HTTPS|HTTP request was sent to HTTPS',
    b'HTTPS|HTTPS|HTTP request to an HTTPS server',
    b'HTTPS|HTTPS|Location: https',
    b'HTTP|HTTP|HTTP/1.1',
    b'HTTP|HTTP|HTTP/1.0',
    b'Zookeeper|Zookeeper|^Zookeeper version: ')


def get_server(port):
    SERVER = {
        '21': 'FTP(Default)',


        '22': 'SSH(Default)',
        '23': 'Telnet(Default)',
        '25': 'SMTP(Default)',
        '53': 'DNS(Default)',
        '68': 'DHCP(Default)',
        '8080': 'HTTP(Default)',
        '69': 'TFTP(Default)',
        '995': 'POP3(Default)',
        '135': 'RPC(Default)',
        '139': 'NetBIOS(Default)',
        '143': 'IMAP(Default)',
        '443': 'HTTPS(Default)',
        '161': 'SNMP(Default)',
        '489': 'LDAP(Default)',
        '445': 'SMB(Default)',
        '465': 'SMTPS(Default)',
        '512': 'Linux R RPE(Default)',
        '513': 'Linux R RLT(Default)',
        '514': 'Linux R cmd(Default)',
        '873': 'Rsync(Default)',
        '888': '宝塔(Default)',
        '993': 'IMAPS(Default)',
        '1080': 'Proxy(Default)',
        '1099': 'JavaRMI(Default)',
        '1352': 'Lotus(Default)',
        '1433': 'MSSQL(Default)',
        '1521': 'Oracle(Default)',
        '1723': 'PPTP(Default)',
        '2082': 'CPanel(Default)',
        '2083': 'CPanel(Default)',
        '2181': 'Zookeeper(Default)',
        '2222': 'DircetAdmin(Default)',
        '2375': 'Docker(Default)',
        '2604': 'Zebra(Default)',
        '3306': 'MySQL(Default)',
        '3312': 'Kangle(Default)',
        '3389': 'RDP(Default)',
        '3690': 'SVN(Default)',
        '4440': 'Rundeck(Default)',
        '4848': 'GlassFish(Default)',
        '5432': 'PostgreSql(Default)',
        '5632': 'PcAnywhere(Default)',
        '5900': 'VNC(Default)',
        '5984': 'CouchDB(Default)',
        '6082': 'varnish(Default)',
        '6379': 'Redis(Default)',
        '9001': 'Weblogic(Default)',
        '7778': 'Kloxo(Default)',
        '10050': 'Zabbix(Default)',
        '8291': 'RouterOS(Default)',
        '9200': 'Elasticsearch(Default)',
        '11211': 'Memcached(Default)',
        '27017': 'MongoDB(Default)',
        '50070': 'Hadoop(Default)'
    }

    for k, v in SERVER.items():
        if k == port:
            return v
    return False

def regex(ip,port,response):
    # match = False
    try:
        # response = response.decode('utf-8')
        # printYellow(response)
        for banner in SIGNS:
            banner = banner.split(b'|')
            # printYellow(banner)
            # banner = banner[-1].decode('utf-8','ignore')
            # printYellow(banner)
            if re.search(banner[-1], response, re.IGNORECASE):
                ban = response.decode('utf-8','ignore')
                # print(ban)
            # if banner in response:
            #     print(banner)

                if 'HTTP' in ban:
                    # print(ban)
                    status = ban.split('\r\n')[0].split(' ')[1]
                    server = ban.split('\r\n')[4].split(':')[1]
                    title = webtitle(str(ip)+':'+str(port))
                    # print(server)

                    #增加打印
                    # print(status)
                    printYellow('ip:{} port:{} banner:{} status:{} server:{} title:{}'.format(ip,port,'HTTP',status,server,title))
                    
                    writer('ip:{} port:{} banner:{} status:{} server:{} title:{}'.format(ip,port,'HTTP',status,server,title))
                    return status
                else:
                    #增加打印
                    printYellow('ip:{} port:{} banner:{} '.format(ip,port,banner[1].decode()))
                    writer('ip:{} port:{} banner:{} '.format(ip,port,banner[1].decode()))
                    return banner[1]
        #增加打印
        if get_server(port):
            banner = get_server(port)
            # printYellow(111)
            printYellow('ip:{} port:{} banner:{} '.format(ip,port,get_server(banner)))
            writer('ip:{} port:{} banner:{} '.format(ip,port,get_server(banner)))
            return banner
        else:

            printYellow('ip:{} port:{} banner:{} '.format(ip,port,response))
            writer('ip:{} port:{} banner:{} '.format(ip,port,response))
            return response

    except:
        pass

if __name__ == '__main__':
    ip = '10.243.73.73'
    port='8500'
    response4 = b'220Authorized users only. All activity may be monitored and reported.\r\n530 Please login with USER and PASS.\r\n'
    response2 = b'HTTP/1.1 400 Bad Request\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: 349\r\nServer: NessusWWW\r\nDate: : Thu, 11 Mar 2021 04:18:41 GMT\r\n\r\n'
    response = b'HTTP/1.1 302 Found\r\nCache-Control: private\r\nContent-Type: text/html; charset=utf-8\r\nLocation: /Security/login?plugin=SecurityPlugin\r\nServer: Microsoft-IIS/7.5\r\nSet-Cookie: ASP.NET_SessionId=z4oucookiujzt22spzh0414f; path=/; HttpOnly\r\nX-AspNetMvc-Version: 4'
    # response2 = b'hhHTTP asdfasdfasdfsdfsf'
    regex(ip,port,response)


    #     printYellow (int('500'))
    # else:
    #     pass
        # server = get_server(port)
        # banner,status = '',''

        # printYellow(banner,server,status)

