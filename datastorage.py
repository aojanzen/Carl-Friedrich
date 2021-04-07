#!/usr/bin/env python3

"""
==============
datastorage.py
==============

Author : Dr. Andreas Janzen
Email  : janzen (at) gmx.net
Date   : 2021-04-07
Version: 1.0

Implements storage of chess tournament data (general, pairings, results) as
json files.
"""


import json
import string


def write_tournament_data(tournament):
    """docstring
    """
    filename = tournament["name"].replace(" ", "_") + ".json"
    with open(filename, "w") as fout:
        fout.write(json.dumps(tournament))


def read_tournament_data(filename):
    """docstring
    """
    filename = filename + ".json"
    with open(filename, "r") as fin:
        tournament = json.loads(fin.read())

    return tournament


# Program starts here
def main():
    pass

if __name__ == "__main__":
    main()

