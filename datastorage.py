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

Functions in datastorage.py:
============================
write_tournament_data(tournament)
    Writes the data contained in the argument tournament into a json file.

read_tournament_data(filename)
    Reads the file "filename" from a json file.

get_tournament_filename()
    Lists the names of all json files in the directory ./data.

switch_stdout(filename = "")
    Switches the standard output between a file "filename" and the screen.
main()
    Just a placeholder, does nothing.
"""


import json
import os
import string
import sys


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


def switch_stdout(filename = ""):
    """docstring
    """
    if filename:
        filename = DATA_PATH + filename
        # Direct standard output to file
        try:
            sys.stdout = open(filename, "w")
        except Exception as e:
            return e
    else:
        # Direct standard output back to screen
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    return "OK"


def main():
    """docstring
    """
    pass


if __name__ == "__main__":
    main()

