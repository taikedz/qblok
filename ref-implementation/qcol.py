#!/usr/bin/env python3

""" Tool to process columnar outputs.

Very rudimentary. Works on `docker ps` and `nmcli con show`

- requires at least two spaces between each header text
- requires header text on a single line
- requires first header character at start of line - no preceding space

Thoughts on improvement:

Use a --headers flag to explicitly specify the names of headers, in order, to be searched for
Use automatic detection if --headers=&NULL
"""

import argparse
import re
import sys

def getWidthsAuto(headerline:str):
    blocks = re.findall('(.+?  +|.+?$)', headerline)
    # ! fails if first header starts with spaces
    # ! fails if space between two headers is a single space
    # e.g. `top -b -n 1 | tail -n+7 | head`
    # that said, `top` uses a very stupid unparsable column layout sometimes
    #   using left-adjusted sometimes using right-adjusted

    read_head = 0
    idx = 0

    # Index positions in the raw line
    positions = [read_head]
    # Map name to cardinal column number
    lookup = {}

    for item in blocks:
        lookup[item.strip()] = idx
        idx += 1

        read_head += len(item)
        positions.append(read_head)

    # The last item is an empty string
    return positions[:-1], lookup


def getWidthsUsing(headers_spec:str, headerline:str):
    headers = [h.replace("\x00", ";") for h in headers_spec.replace("\\;", "\x00").split(";") if h.strip()]
    read_head = 0
    idx = 0
    positions = []
    lookup = {}

    for current_h, next_h in thisAndNextIn(headers):
        # Note we have n'th column under the given header
        lookup[current_h] = idx
        idx += 1

        # Current read head is at current header
        positions.append(read_head)
        # Go beyond it
        read_head = headerline.find(current_h, read_head) + len(current_h)
        # And find start of next - we'll start there next time.
        read_head = headerline.find(next_h, read_head)

    # Last item gets missed by the iteration
    lookup[next_h] = idx
    positions.append(read_head)

    # The last item is an empty string
    return positions, lookup

def thisAndNextIn(items):
    i=0
    while i<len(items)-1:
        yield items[i], items[i+1]
        i += 1


def extract(positions:list[int], dataline:str):
    idx = 0
    items = []
    nextstop = 0
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


def liftValuesFor(keys, dataline, lookup):
    values = []
    if not keys:
        return dataline

    for key in keys:
        idx = lookup.get(key)
        assert idx is not None, f"Invalid header '{key}'"
        values.append(dataline[idx])
    return values


def example_readinputs():
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

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("column_sel", help="Columns to select", nargs="*")
    parser.add_argument("--headers", help="Semi-colon separated column names", default=None)
    parser.add_argument("--ex", "-E", help="Use example data", action="store_true")
    return parser.parse_args()

def main():
    args = parseArgs()
    print(args)

    if args.ex:
        h_line, d_lines = example_readinputs()
    else:
        h_line, d_lines = readinputs()

    if args.headers:
        positions,lookup = getWidthsUsing(args.headers, h_line)
    else:
        positions,lookup = getWidthsAuto(h_line)

    print(f"{positions} : {lookup}")

    for line in [extract(positions, line) for line in d_lines if line]:
        print(liftValuesFor(args.column_sel, line, lookup))


try:
    main()
except AssertionError as e:
    print(e)
    exit(1)

