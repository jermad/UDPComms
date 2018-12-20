#!/usr/bin/env python3

import sys
import argparse
import json
import time
import select

import UDPComms


def peek_func(port):
    sub = UDPComms.Subscriber(port, timeout = 10)
    while 1:
        try:
            data = sub.recv()
            print( json.dumps(data) )
        except UDPComms.timeout:
            exit()

def poke_func(port, rate):
    pub = UDPComms.Publisher(port, local = True)
    data = None

    while 1:
        time.sleep( rate/1000 )

        if select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line.rstrip():
                data = line.rstrip()
                continue

        if data != None:
            pub.send( json.loads(data) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    peek = subparsers.add_parser("peek")
    peek.add_argument('port', help="UDP port to subscribe to", type=int)

    poke = subparsers.add_parser("poke")
    poke.add_argument('port', help="UDP port to publish the data to", type=int)
    poke.add_argument('rate', help="how often to republish (ms)", type=float)

    args = parser.parse_args()

    print(args)

    if args.subparser == 'peek':
        peek_func(args.port)
    elif args.subparser == 'poke':
        poke_func(args.port, args.rate)
    else:
        parser.print_help()




