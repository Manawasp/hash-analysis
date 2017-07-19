#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cityhash import CityHash128 as ch

# open file and hash each line
def hash_from_file(filename, constraint):
    hashs = []
    with open(filename, 'r') as f:
        for line in f:
            if (constraint):
                hashs.append(ch(line) % constraint)
            else:
                hashs.append(ch(line))
    return hashs

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
    print("Hash: {:,}   ||   Duplicate: {:,}   ||   {}%".format(len(hashs), duplicat, duplicat / len(hashs) * 100))

def main():
    hashs = hash_from_file("read.txt", 62 ** 6)
    hashs.sort()
    duplicat = find_duplication(hashs)
    print_result(hashs, duplicat)

if __name__ == "__main__":
    main()
