from scapy import main
from scapy.all import *
import sys, socket

def get_local_net():
    #获取主机名
    hostname = socket.gethostname()
    print('主机名:' + hostname)
    #获取主机的局域网所有ip
    localallip = socket.gethostbyname_ex(hostname)
    #遍历所有主机ip，选择网卡
    while True:
        for Allip in localallip[2]:
            print(Allip)
        hostip = input('####请选择主机的IP地址####\n')
        if hostip in localallip[2]:
            print('####开始扫描####')
            result = get_vlan_ip_and_mac(hostip)
            return result
            break               
        else:
            print('####请输入正确的IP####')
#扫描函数
def get_vlan_ip_and_mac(hostip):
    #提取网段
    localipnums = hostip.split('.')
    scanipnat = localipnums[0] + '.' + localipnums[1] + '.' + localipnums[2]
    result = []
    #遍历扫描所有网段的IP，进行扫描
    for i in range(1,255):
        scanip = scanipnat + '.' + str(i)
        arpPkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=scanip)
        res = srp1(arpPkt,timeout=0.1, verbose=0)
        print('正在扫描' + scanip)
        if res :
            result.append({"localIP":res.psrc,"mac":res.hwsrc})
            print(result)
    return result

if __name__=='__main__':
    result = get_local_net()
    for i in result:
        print(i)
    print('####扫描结束####')