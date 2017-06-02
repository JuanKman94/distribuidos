#!/usr/bin/env python3

import sys
import time
import automata

try:
    sys.index('server')
    nier = automata(port = 9000)
    nier.become_master()
except:
    'nada'

while True:
    try:
        nier = automata.automata(port = 9000)
        master_ip = nier.beacon()

        if not master_ip:
            print('No master found. Becoming one...')
            nier.become_master()
        else:
            print('master found {0}. pinging...'.format(master_ip))
            resp = nier.ping()

            if not resp: nier.close()

    except:
        print('Some error happened. Whatever, sleeping 5...')
        time.sleep(5)
