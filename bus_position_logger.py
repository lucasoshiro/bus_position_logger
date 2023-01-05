#!/usr/bin/env python3

import requests
import logging
from time import sleep,time
from pprint import pprint
from argparse import ArgumentParser
from datetime import datetime
from collections import namedtuple

BASE_URL = 'http://api.olhovivo.sptrans.com.br/v2.1/'
POSICAO_LINHA = '/Posicao/Linha'
LOGIN_AUTENTICAR = '/Login/Autenticar'
LINHA_BUSCAR = '/Linha/Buscar'

INTERVAL = 10

Entry = namedtuple('Entry', ' '.join(['timestamp', 'line', 'prefix', 'lat', 'lng']))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

cookies = dict()
line_cls = dict()

output_file = None
args = None

def authenticate(key):
    global cookies

    ok = False

    while not ok:
        try:
            response = requests.post(
                url=BASE_URL + LOGIN_AUTENTICAR,
                params={'token': key}
            )

            cookies = response.cookies
            ok = response.ok
        except:
            sleep(1)

    return response.cookies

def call_endpoint(endpoint, **params):
    global cookies

    response = None
    status_code = 401

    while status_code == 401:
        try:
            response = requests.get(
                url=BASE_URL + endpoint,
                params=params,
                cookies=cookies
            )

            status_code = response.status_code
        except:
            authenticate(args.key)
            sleep(1)

    return response.json() if response and response.ok else None

def get_line_cls(line):
    logging.info(f'Get cls for line {line}')
    json = call_endpoint(LINHA_BUSCAR, termosBusca=line)

    if not json:
        raise LookupError(f'Line {line} not found')

    cls = (*(line['cl'] for line in json),)

    logging.info(f'cls for line {line}: {" ".join(map(str, cls))}')

    return cls

def get_buses_in_line(line):
    logging.info(f'Get bus positions for line {line}')

    for cl in line_cls[line]:
        json = call_endpoint(POSICAO_LINHA, codigoLinha=cl)
        buses = json['vs']

        for bus in buses:
            timestamp = datetime.fromisoformat(bus['ta'][:-1]).timestamp()
            prefix = bus['p']
            lat, lng = bus['py'], bus['px']

            entry = Entry(timestamp, line, prefix, lat, lng)
            output_file.write(','.join(map(str, entry)))
            output_file.write('\n')

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='Bus position logger',
        description='Log the positions of the buses in São Paulo'
    )

    parser.add_argument('-k', '--key')
    parser.add_argument('-o', '--output')
    parser.add_argument('-l', '--lines', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    logging.info('Start!')

    output_file = open(args.output, 'w')

    logging.info(f'Writing to {args.output}')    

    output_file.write(','.join(Entry._fields))
    output_file.write('\n')

    authenticate(args.key)
    line_cls = {line: get_line_cls(line) for line in args.lines}

    while True:
        for line in args.lines:
            get_buses_in_line(line)
        sleep(INTERVAL)

