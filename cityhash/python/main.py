#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from cityhash import CityHash128 as ch

# open file and hash each line
def hash_from_file(filename, constraint, max_read):
    hashs = []
    try:
        f = open(filename, 'r')
    except IOError:
        print("Error: file not found")
        return hashs, True
    else:
        with f:
            count = 0
            for line in f:
                if max_read != 0 and count >= max_read:
                    print("- Stop to read file after {:,} lines".format(count))
                    break;
                if (constraint):
                    hashs.append(ch(line) % constraint)
                else:
                    hashs.append(ch(line))
                count += 1
    return hashs, False

def find_duplication(hashs):
    duplicat = 0
    for i, h in enumerate(hashs):
        if i + 1 >= len(hashs):
            break
        n = hashs[i + 1]
        if n == h:
            duplicat += 1
    return duplicat

def print_result(hashs, duplicat):
    print("= Hash: {:,}\n= Duplicate: {:,}\n= Rate: {:.2f}%".format(len(hashs), duplicat, duplicat / len(hashs) * 100))

def main(parser):
    args = parser.parse_args()
    print('- Applied constraint {:,}'.format(args.constraint))
    hashs, err = hash_from_file(args.file[0], args.constraint, args.max)
    if len(hashs) == 0:
        if err is False:
            print("Error: no value found from the file")
        return
    hashs.sort()
    duplicat = find_duplication(hashs)
    print_result(hashs, duplicat)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        nargs=1,
                        type=str,
                        help="Dest file of urls")
    parser.add_argument("-c",
                        "--constraint",
                        type=int,
                        default=62 ** 6,
                        help="Constraint force hash to be contained in a range")
    parser.add_argument("-m",
                        "--max",
                        type=int,
                        default=0,
                        help="Max read of line")
    main(parser)
