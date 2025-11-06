#!/usr/bin/env python3

""" Tool to process columnar outputs.

Very rudimentary. Works on `docker ps` and `nmcli con show`

- requires at least two spaces between each header text
- requires header text on a single line
- requires first header character at start of line - no preceding space
"""

import re
import sys

def getWidths(headerline:str):
    blocks = re.findall('(.+?  +|.+?$)', headerline)
    # ! fails if first header starts with spaces
    # ! fails if space between two headers is a single space
    # e.g. `top -b -n 1 | tail -n+7 | head`

    read_head = 0
    positions = [read_head]
    lookup = {}
    idx = 0
    for item in blocks:
        lookup[item.strip()] = idx
        idx += 1
        read_head += len(item)
        positions.append(read_head)

    # The last item is an empty string
    return positions[:-1], lookup


def extract(positions:list[int], dataline:str):
    idx = 0
    items = []
    while idx < len(positions)-1:
        readhead = positions[idx]
        nextstop = positions[idx+1]
        items.append(dataline[readhead:nextstop].strip())
        idx +=1
    items.append(dataline[nextstop : len(dataline)].strip())
    return items

def readinputs():
    lines = sys.stdin.readlines()
    return lines[0], lines[1:]


def lift(keys, dataline, lookup):
    values = []
    if not keys:
        return dataline

    for key in keys:
        idx = lookup.get(key)
        assert idx is not None, f"Invalid header '{key}'"
        values.append(dataline[idx])
    return values


def example():
    h_line  = "ONE   TWO   THREE AND FOUR    FIVE"
    d_lines = [
              "cat   meow  Melissa           good",
              "dog   woof  Baxter            chaos",
              "mouse eep   unnamed           wild",
              "",
              "incomplete",
              ]
    print(h_line)
    for line in d_lines:
        print(line)
    print("---")
    return h_line, d_lines


def main():
    #h_line, d_lines = example()
    h_line, d_lines = readinputs()
    positions,lookup = getWidths(h_line)
    for line in [extract(positions, line) for line in d_lines if line]:
        print(lift(sys.argv[1:], line, lookup))


try:
    main()
except AssertionError as e:
    print(e)
    exit(1)

