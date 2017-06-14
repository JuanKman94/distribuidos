#!/usr/bin/env python3

import sys
import json
import time
import psutil
import netaddr
import platform
import netifaces
import threading as ting
import socket as sock

PORT = 3000
MAX_CON = 5
MAX_MSG_LEN = 512
MAX_FAILED_ATTEMPTS = 10

class automata(sock.socket):
    def __init__(self, address = '0.0.0.0', port = PORT, max_conn = MAX_CON):
        self.address = address
        self.port = port
        self.max_conn = max_conn
        self.pals = dict() # other automatas found

        try:
            # AF_INET for IPv4
            # SOCK_STREAM for TCP, SOCK_DGRAM for UDP
            super().__init__( sock.AF_INET, sock.SOCK_DGRAM )
        except sock.error as ex:
            print('Error creating socket. {0}'.format(ex))

    def beacon(self, addr):
        '''Send beacon to entire network to look for other automatas'''
        print('broadcasting CPU data on port {p}'.format(p = addr[1]))
        try:
            while True:
                data = json.dumps(get_cpu_data()).encode()
                self.sendto(data, addr)
                time.sleep(3)
        except Exception as ex:
            print('error [{t}]!'.format(t = ting.current_thread().name), ex)

    def up(self):
        try:
            print('listening on port {p}'.format(p = self.port))
            self.bind( ('0.0.0.0', self.port) )

            while True:
                conn = self.recvfrom(MAX_MSG_LEN) # blocking call
                ip = conn[1][0]
                try:
                    data = json.loads(str(conn[0], encoding='utf-8'))
                except Exception as ex:
                    data = { "error": str(ex) }

                self.pals[ip] = data
        except Exception as ex:
            print('error [{t}]!'.format(t = ting.current_thread().name), ex)

def get_cpu_data():
    mem, arch = psutil.virtual_memory(), platform.machine()
    os, proc = platform.system(), platform.processor()

    return {
        'mem': {
            'total': mem.total,
            'available': mem.available,
            'active': mem.active,
            'percent': mem.percent
        },
        'os': os,
        'proc': proc,
        'ts': time.gmtime()
    }

def get_ifaces():
    '''Return dictionary with each interface as a key and another
    dictionary with netmask and address as value'''
    ifaces = netifaces.interfaces()
    info = {}

    for i in range( len(ifaces) ):
        iface = ifaces[i]
        addresses = netifaces.ifaddresses(iface)
        info[ iface ] = {}

        try:
            inet = addresses[ sock.AF_INET ][0]

            # skip loopback -- just raise error, fuck it
            if inet['addr'] == '127.0.0.1': raise KeyError

            info[iface]['addr'] = inet['addr']
            info[iface]['netmask'] = inet['netmask']
            info[iface]['broadcast'] = inet['broadcast']
        except KeyError as err:
            del info[ iface ]
            continue

    return info
