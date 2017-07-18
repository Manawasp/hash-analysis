#!/usr/bin/python3
import argparse
import string
import sys

from hashids import Hashids

# Global vars
base = string.ascii_letters + string.digits

def search(hashids, length):
    bmax = len(base) ** length
    vmin = 0
    vmax = bmax
    print('Hash possibilities: {:,}'.format(vmax))

    while (vmax - vmin) > 1:
        delta = int((vmin + vmax) / 2)
        if len(hashids.encode(delta)) > length:
            vmax = delta
        else:
            vmin = delta
    print('Breaking point: {:,}'.format(vmax))
    print('Loss: {0:.2f}%'.format(((bmax - vmin) / bmax) * 100))
    return vmax

def line_message(msg):
    sys.stdout.write('\r{}'.format(msg))
    sys.stdout.flush()

def ensure(hashids, length, value):
    for i in range(0, value):
        if len(hashids.encode(i)) > length:
            clean_line('Ensure: KO. Mismatched result found: {:,}\n'.format(i))
            return i
        if i % 17 == 0:
            line_message('Ensure: {0:.2f}%'.format((i / value) * 100))
    line_message('Ensure: done\n')
    return value

def main(parser):
    args = parser.parse_args()
    hashids = Hashids(salt=args.salt, min_length=args.length)
    value = search(hashids, args.length)

    if args.ensure:
        value = ensure(hashids, args.length, value)

if __name__ == "__main__":
    # Global parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-l",
                        "--length",
                        type=int,
                        default=6,
                        help="min length of hashids")
    parser.add_argument("-s",
                        "--salt",
                        type=str,
                        default="",
                        help="hashids salt")
    parser.add_argument("-e",
                        "--ensure",
                        type=bool,
                        default=False,
                        help="ensure there between 0 and the given number there is no length mismatch")
    main(parser)
