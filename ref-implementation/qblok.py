#!/usr/bin/env python3

import os
import sys
import pathlib
import argparse

THIS = pathlib.Path(os.path.realpath(__file__))
HEREDIR = pathlib.Path(os.path.dirname(THIS))


def cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", "-L", type=int, default=0, help="Level to start splitting blocks at. Default is zero, no splitting")
    args = parser.parse_args()
    return args


class LevelTracker:
    def __init__(self, target_level):
        self._data = {}
        self._target_level = target_level
        self._cur_level = 0
        self._current_data_lines = []

    def commit(self):
        if self._cur_level not in self._data:
            self._data[self._cur_level] = []
        self._data[self._cur_level].append(self._current_data_lines)
        self._current_data_lines = []

    def append(self, data):
        self._current_data_lines.append(data)

    def setLevel(self):
        pass


def main():
    args = cli_args()

    levels = {0:[]}
    current_level

    for line in sys.stdin.readlines():
        line = line.rstrip()

        print(repr(line))


# Generic launch and catch assertions
if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        # Catches all exceptions, but not KeyboardInterrupt

        # Normally silence tracebacks. Run with PY_TRACEBACK=true to show them
        if os.getenv("PY_TRACEBACK") == "true":
            raise
        else:
            print(e)
            exit(1)
