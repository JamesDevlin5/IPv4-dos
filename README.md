# Denial-of-Service Script

This script takes a target host address and floods it with custom IP packets that slow the receiver's network capabilities to a halt.
**This only works on IP version 4.**

## How It Works

IPv4 packets can be fragmented by arbitrary hops on the way to their destination.
To indicate that a received packet has been fragmented and needs to be put back together by the receiver, a flag in the IP header is set.
Thus, the receiver is forced to wait for the rest of the packet fragment before it can be processed.
This script, however, will not send the rest of the packet and the receiver will have to eventually timeout the data.
This can overwhelm the target and exhaust most of its networking capabilities.

## Usage

This script uses raw sockets to manipulate the outgoing IP headers.
Most operating systems will not allow this behavior unless you are a privileged user, so you will likely need to prefix this script with `sudo`.

