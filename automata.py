#!/usr/bin/env python3

import sys
import json
import time
import psutil
import netaddr
import platform
import netifaces
import socket as sock

MAX_FAILED_ATTEMPTS = 10

class automata(sock.socket):
    def __init__(self, address = '', port = 9999, max_conn = 5):
        self.address = address
        self.port = port
        self.max_conn = 5
        self.role = 'server' # [ server | master ]
        self.master = None # ip address for current master
        self.ifaces = None

        try:
            # AF_INET for IPv4
            # SOCK_STREAM for TCP, SOCK_DGRAM for UDP
            super().__init__( sock.AF_INET, sock.SOCK_STREAM )
        except sock.error as ex:
            print('Error creating socket. {0}'.format(ex))

    def beacon(self):
        '''Send beacon to entire network to look for other automatas'''
        ifaces = self.get_ifaces()
        self.master = None

        for iface in ifaces:
            cidr = netaddr.IPNetwork(ifaces[iface]['addr'], ifaces[iface]['netmask'])

            if self.master: break

            hosts = [ ip for ip in cidr.iter_hosts() ]
            #hosts = hosts[210:220] # testing

            for ip in hosts:
                print('connecting {ip}... '.format(ip = ip), end='')
                try:
                    self.connect( (str(ip), self.port) )
                    print('successful')
                    self.master = str(ip)
                    break
                except ConnectionRefusedError:
                    print('refused')
                except OSError as ex:
                    print('no route [{0}]'.format(ex))
                else:
                    print('error')

        return self.master

    def up(self):
        try:
            self.bind( (self.address, self.port) )
            self.listen(self.max_conn)
            print('Socket binded on {0}:{1}'.format(self.address, self.port))

            while True:
                (conn, addr) = self.accept() # blocking call

                print('Connected with {0}'.format(addr[0]))

                data = str(conn.recv(1024), encoding='utf-8')
                while data:
                    print(data)
                    conn.sendall('OK\r\n'.encode())
                    data = str(conn.recv(1024), encoding='utf-8')

                print('Closing connection with {0}'.format(addr[0]))
                conn.close()
        except:
            print('Closing server socket. Sleeping 10 seconds...')
            self.close()
            time.sleep(10)
            return 1

    def ping(self):
        '''Send info to master'''
        count, failed_attempts = 0, 0
        failure, no_master_found = False, False

        while True:
            try:
                message = str( get_cpu_data() )
                self.sendall(message.encode())
            except Exception as ex:
                failure = True

            if failure:
                failed_attempts += 1
            else:
                reply = str(self.recv(1024), encoding = 'utf-8')
                print(count, '. ', reply.rstrip() )
                count += 1
                time.sleep(1)

            if failed_attempts >= MAX_FAILED_ATTEMPTS:
                no_master_found = True
                break

        return None

    def is_master(self):
        return self.role == 'master'

    def become_master(self):
        self.role = 'master'
        self.address = self.get_ipv4()

        if not self.address:
            print('Error getting IPv4 address.')
            sys.exit(1)

        self.up()

    def get_ifaces(self):
        '''Return dictionary with each interface as a key and another
        dictionary with netmask and address as value'''
        if self.ifaces: return self.ifaces

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
            except KeyError as err:
                del info[ iface ]
                continue

        self.ifaces = info
        return info

    def get_ipv4(self):
        ifaces = self.get_ifaces()
        for iface in ifaces:
            cidr = netaddr.IPNetwork(ifaces[iface]['addr'], ifaces[iface]['netmask'])
            try:
                cidr.ipv4() # is it a IPv4 network?
                return ifaces[iface]['addr']
            except netaddr.AddrConversionError:
                return None

        return None

def get_cpu_data():
    mem, arch = psutil.virtual_memory()[0], platform.machine()
    os, proc = platform.system(), platform.processor()

    mem /= 1024
    mem /= 1024
    mem /= 1024

    return {
            #'hdd': '32GB',
            'mem': str(mem) + 'GB',
            #'arch': arch,
            'os': os,
            'proc': proc
    }
