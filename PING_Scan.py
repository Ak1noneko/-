# -*- coding:utf-8 -*-
from multiprocessing import process
from scapy.all import *
from random import randint
import time
import ipaddress
import multiprocessing


def scapy_scan_one(host):
    id_ip = randint(1, 65535)
    seq_ping = randint(1, 65535)
    id_ping = randint(1, 65535)
    packet = IP(dst=host, ttl=128, id=id_ip) / ICMP(id=id_ping, seq=seq_ping) / b'hello everyone'
    ping = sr1(packet, timeout=0.2, verbose=False)

def scapy_ping_scan(network):
    net = ipaddress.ip_network(network)
    ip_processe = {}
    for ip in net:
        ip_addr = str(ip)
        ping_one = multiprocessing.Process(target = scapy_scan_one,args = (ip_addr,))
        ping_one.start()
        ip_processe[ip_addr] = ping_one
    ip_list = []
    for ip, process in ip_processe.items():
        if process.exitcode == 3:
            ip_list.append(ip)
        else:
            process.terminate()
    return sorted(ip_list)


if __name__ == '__main__':
    needToscan = input('请输出扫描的网段，如192.168.1.0/24\n')
    t1 = time.time()
    active_ip = scapy_ping_scan(needToscan)
    print('存活的IP地址：')
    for ip in active_ip:
        print(ip)
    t2 = time.time()
    print('用时：{}s' .format(int(t2-t1)))