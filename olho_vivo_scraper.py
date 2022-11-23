#!/usr/bin/env python3

import requests
from time import sleep,time
from pprint import pprint
from argparse import ArgumentParser

BASE_URL = 'http://api.olhovivo.sptrans.com.br/v2.1'
POSICAO_LINHA = '/Posicao/Linha'
AUTENTICAR = '/Login/Autenticar'

IDA = '2085'
VOLTA = '34853'

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='Olho Vivo',
        description='Olho Vivo'
    )

    parser.add_argument('-k', '--key')
    parser.add_argument('-o', '--output')
    parser.add_argument('-l', '--lines', nargs='+')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    print(args.key)
    print(args.output)
    print(args.lines)
    print(args.verbose)
