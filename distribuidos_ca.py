import socket as sock
import threading
import json

class server(sock.socket):
    def __init__(self, address = '', port = 3000, max_con = 10):
        self._address = address
        self._port = port
        self._max_con = max_con

        try:
            # AF_INET for IPv4
            # SOCK_STREAM for TCP, SOCK_DGRAM for UDP
            super().__init__( sock.AF_INET, sock.SOCK_STREAM )
        except sock.error as ex:
            print('Error creating socket. {0}'.format(ex))
    
    def up(self):
        try:
            self.bind( (self._address, self._port) )
            self.listen(self._max_con)
            print('Socket binded on {0}:{1}'.format(self._address, self._port))
        except sock.error as ex:
            print('Error binding socket. {0}'.format(ex))

    def handle_conn(self, conn, addr):
        #conn.send('Receiving data...\r\n'.encode())
        data = ''

        while True:
            tmp = str( conn.recv(1024), encoding = 'utf-8' ).strip()
            if not tmp or tmp == '': break
            data += tmp

        try:
            data = self.parse_stats( data )
        except json.JSONDecodeError as ex:
            print('Error parsing data from {0}'.format(addr[0]))

        conn.sendall('OK\r\n'.encode())
        conn.close()
        print('Received data from {ip}:{port} => {data}'.format(
            ip = addr[0],
            port = addr[1],
            data = data
        ))

        return (addr, data)

    def parse_stats(self, data = ''):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as ex:
            print('Invalid JSON data => {0}'.format(ex.doc))

        return data
