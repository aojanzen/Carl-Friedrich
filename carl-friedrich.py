#!/usr/bin/env python3

"""
carl-friedrich.py

Autor: Dr. Andreas Janzen
Email: janzen (at) gmx.net
Date : 2021-04-07

A command line app to organize round-robin chess tournaments

Player details can be loaded from the website of the German Chess Association,
pairings will be set according to the Berger tables that the FIDE recommends.
Data is stored locally in the form of json files.
"""


import sys

from tournament import create_new_tournament, load_tournament, print_pairings,\
                       update_result, refresh_scores


# Global variable to store current tournament data
current_tournament = None


def hello():
    print("\n\nNOT YET IMPLEMENTED!\n\n")


def enter_results():
    """docstring
    """
    # current_tournament shall be changed in this function
    global current_tournament

    if not current_tournament:
        print("\nBitte laden Sie zunächst ein Turnier, oder legen Sie ein neues"
              " Turnier an.")
    else:
        print("\nBitte waehlen Sie die Runde, für die Sie Ergebnisse eingeben",
              " möchten.")
        while True:
            R = input("\nRunde > ")
            if R.isnumeric():
                R = int(R)
                break
        print_pairings(current_tournament, R)

        while True:
            print("Bitte waehlen Sie eine Partie, oder geben Sie eine 0 ein,"
                  "um zum\nHauptmenue zurueckzukehren.")
            game = input("\nPartie > ")
            if game.isnumeric():
                game = int(game)
                break
        if game == 0:
            return

        print("\nBitte geben Sie das Ergebnis ein (1,0,=,+,- oder C für eine "
              "ausgefallene Partie.)\n")
        while True:
            result = input("Ergebnis > ")
            if result[0] in "10=+-C":
                result = result[0]
                break

        current_tournament = update_result(current_tournament, R, game, result)


def print_standings(tournament):
    """docstring
    """
    print("\n\n")
    tournament = refresh_scores(tournament)


def main_menu():
    """docstring
    """
    # current_tournament shall be changed in this function
    global current_tournament

    menu = {
                "1": "Neues Turnier anlegen",
                "2": "Bestehendes Turnier laden",
                "3": "Paarungen anzeigen und Ergebnisse eingeben",
                "4": "Tabelle anzeigen",
                "5": "Daten als Textdatei exportieren",
                "6": "Programm beenden"
           }

    print("\n"*5)
    print("===========================")
    print("=== CARL-FRIEDRICH V1.0 ===")
    print("===========================")
    print("Andreas Janzen, 2021-04-05\n")

    print("==================")
    print("=== Hauptmenue ===")
    print("==================")
    print()

    for key, value in menu.items():
        print(f"({key}) {value}")

    while True:
        choice = input("\nBitte waehlen Sie einen Menuepunkt > ")
        if choice in list("123456"):
            if choice == "1":
                current_tournament = create_new_tournament()
            elif choice == "2":
                current_tournament = load_tournament()
            elif choice == "3":
                enter_results()
            elif choice == "4":
                print_standings(current_tournament)
            elif choice == "5":
                hello()
            elif choice == "6":
                sys.exit()
        break # Leave input loop if user entered a valid choice


def main():
    while True:
        main_menu()


if __name__ == "__main__":
    main()

