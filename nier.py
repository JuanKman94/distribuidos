#!/usr/bin/env python3

import sys
import time
import random
import automata

try:
    pos = sys.argv.index('--port')
    PORT = int(sys.argv[pos+1])
except:
    PORT = 9000

try:
    sys.argv.index('--server')
    nier = automata.automata(port = PORT)
    nier.become_master()
except:
    'Could not become master'

while True:
    lost_master = False

    try:
        nier = automata.automata(port = PORT)
        master_ip = nier.beacon()

        try:
            if not master_ip and master_ip != '':
                print('No master found. Becoming one...')
                nier.become_master()
        except:
            'nada'

        #print('master found {0}. pinging...'.format(master_ip))
        if master_ip == '':
            lost_master = nier.ping('')

        if lost_master: nier.become_master()

    except Exception as ex:
        print(ex)
        time.sleep(5)
        nier.close()
