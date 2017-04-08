#!/usr/bin/env python
# python 3.5

import socket
import time
import sys
import platform
import psutil

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

try:
    # AF_INET for IPv4
    # SOCK_STREAM for TCP, SOCK_DGRAM for UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as ex:
    print('Failed to create socket. Error {0}'.format(ex))
    sys.exit(1)

print('Socket created!')

host = 'google.com'
port = 80

#try:
#    remote_ip = socket.gethostbyname(host)
#except Exception as ex:
#    print('Could not resolve hostname')
#    sys.exit(1)

#print('IP address of {hostname}: {ip}'.format(hostname = host, ip = remote_ip))

remote_ip, port = '', 3000
s.connect( (remote_ip, port) )
print('Connected to {0}!'.format(host))

while True:
    try:
        message = str( get_cpu_data() )
        s.sendall(message.encode())
    except Exception as ex:
        print('Send failed. {0}'.format(ex))
        sys.exit(1)

    print('Message sent successfully. Response:\n')

    reply = s.recv(4096)
    print( str(reply, encoding = 'utf-8' ) )
    time.sleep(1)

s.close()
