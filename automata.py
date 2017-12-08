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

PAIR_MSG = 'PAIRING'
TCP_PORT = 3000
UDP_PORT = 3333
MAX_CON = 5
MAX_MSG_LEN = 512
MAX_FAILED_ATTEMPTS = 10
INTERVAL = 3

class automata(sock.socket):
    def __init__(self, address = '0.0.0.0', max_conn = MAX_CON):
        self.address = address
        self.max_conn = max_conn
        self.peers = dict() # other automatas found

        try:
            # AF_INET for IPv4
            # SOCK_STREAM for TCP, SOCK_DGRAM for UDP
            super().__init__( sock.AF_INET, sock.SOCK_DGRAM )
        except sock.error as ex:
            print('Error creating socket. {0}'.format(ex))

    def beacon(self):
        '''Send beacon to entire network to look for other automatas
        using UDP: 255.255.255.255 on port UDP_PORT
        '''
        # sleep to avoid weird race condition that returns errno 22
        time.sleep(INTERVAL)
        addr = ( '255.255.255.255', UDP_PORT)
        print('INFO Broadcasting on UDP', addr)
        while True:
            try:
                #data = json.dumps(get_cpu_data()).encode()
                self.sendto(PAIR_MSG.encode(), addr)
                time.sleep(INTERVAL)
            except Exception as ex:
                print('ERROR {t}:'.format(t = ting.current_thread().name), ex)

    def listen(self):
        '''Listen to entire network for others automatas using UDP'''
        print('INFO Listening on UDP {0}:{1}'.format(self.address, UDP_PORT))
        try:
            self.bind( ('', UDP_PORT) )
        except sock.error as msg:
            print('Bind failed.', msg)
            sys.exit(1)

        while True:
            try:
                conn = self.recvfrom(MAX_MSG_LEN) # blocking call
                ip = conn[1][0]
                msg = str(conn[0], encoding='utf-8')

                if msg != PAIR_MSG:
                    try:
                        data = json.loads(msg)
                    except json.decoder.JSONDecoderError:
                        print('ERROR Bad format')
                        continue

                if self.address != ip:
                    self.connect_peer(ip)
            except sock.timeout:
                ''

    def listen_peer(self):
        print('INFO Listening on TCP {0}:{1}'.format(self.address, TCP_PORT))
        tcp = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        tcp.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        tcp.bind((self.address, TCP_PORT))
        tcp.listen(10)

        while 1:
            try:
                conn, addr = tcp.accept()
                data = get_cpu_data()
                data['ip'] = self.address
                data = str.encode(json.dumps(data))

                conn.sendall(data)
                conn.close()
            except sock.timeout:
                ''

        tcp.close()

    def connect_peer(self, ip):
        if not self.peers.get(ip, None):
            s = None
            try:
                s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
                s.connect((ip, TCP_PORT))
            except Exception as ex:
                if s: s.close()
                print('ERROR connect_peer:', ex)
                return False

            resp = s.recv(1024)
            self.peers[ip] = resp
            s.close()

        return True

    def delete(self, ip):
        '''Remove peer (IP) from list of peers'''
        try:
            if self.peers.get(ip, None):
                self.peers.pop(ip)
            return True
        except:
            return False

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
