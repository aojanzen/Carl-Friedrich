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
import os
import string
import sys

# from carl-friedrich import xx


DATA_PATH = "./data/"


def write_tournament_data(tournament):
    """Writes the tournament data (general, pairings, results, NO standings!)
    to a json file. Returns "OK" if no error occurred, otherwise returns the
    error message.
    """
    filename = DATA_PATH + tournament["name"].replace(" ", "_") + ".json"
    try:
        with open(filename, "w") as fout:
            fout.write(json.dumps(tournament))
    except Exception as e:
        return e

    return "OK"


def read_tournament_data(filename):
    """Reads tournament data (general, player list, pairings, results, but no
    standings) from a json file into a dictionary. Returns the dictionary if
    no error occurred, otherwise returns the error message.
    """
    filename = DATA_PATH + filename
    try:
        with open(filename, "r") as fin:
            tournament = json.loads(fin.read())
    except Exception as e:
        return e

    return tournament


def get_tournament_filename():
    """Prints a list of all .json files in the data folder defined by DATA_PATH
    and lets the user chose a file. The filename is the returned to the caller.
    """
    print("\n\nLade Turnierdaten")
    print("=================\n")

    files = os.listdir(DATA_PATH)
    for i, f in enumerate(files, 1):
        if f.endswith(".json"):
            print(f"{i:3d} -- {f.split('.')[0].replace('_', ' '):25s}")

    choice = input("\nBitte waehlen Sie ein Turnier aus > ")
    filename = files[int(choice) - 1]

    return filename


def write_pairings_to_file(tournament, R):
    """docstring
    """
    filename = DATA_PATH + tournament["name"].replace(" ", "_") + f"_R{R}_" + \
               ".txt"

    # Direct standard output to file
    try:
        sys.stdout = open(filename, "w")
    except Exception as e:
        return e

    tmp_str = f"Zwischenstand vor Runde {R}"
    print(tmp_str)
    print("=" * len(tmp_str))

    # Direct standard output back to screen
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    return None


def main():
    """docstring
    """
    pass


if __name__ == "__main__":
    main()

