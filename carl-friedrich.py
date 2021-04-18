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
        update_result, refresh_scores, print_standings, write_pairings_to_file


# Define global variable to hold the current tournament data
current_tournament = None


def enter_results(tournament):
    """docstring
    """
    if not tournament:
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

        print_pairings(tournament, R)

        while True:
            print("Bitte waehlen Sie eine Partie, oder geben Sie eine 0 ein,"
                  "um zum\nHauptmenue zurueckzukehren.")
            game = input("\nPartie > ")
            if game.isnumeric():
                game = int(game)
                break
        if game == 0:
            return tournament

        print("\nBitte geben Sie das Ergebnis ein (1,0,=,+,- oder C für eine "
              "ausgefallene Partie.)\n")
        while True:
            result = input("Ergebnis > ")
            if result[0] in "10=+-C":
                result = result[0]
                break

        tournament = update_result(tournament, R, game, result)

        return tournament


def print_standings_menu(tournament):
    """docstring
    """
    tmp_str = "Tabelle anzeigen"
    print("\n"+tmp_str)
    print("=" * len(tmp_str))

    print("Bitte waehlen Sie eine Runde, nach der der Tabellenstand\nangezeigt",
          "werden soll.\n")
    while True:
        R = input("Runde > ")
        if R.isnumeric():
            R = int(R)
            break

    tournament = refresh_scores(tournament, R)
    print_standings(tournament, R)

    return None


def export_pairings(tournament):
    """docstring
    """
    tmp_str = "Exportiere Zwischenstand und Rundenpaarungen in Textdatei"
    print("\n\n" + tmp_str)
    print("=" * len(tmp_str))
    print("\nDie Paarungen welcher Runde sollen exportiert werden?\n")

    while True:
        R = input("Runde > ")
        if R.isnumeric():
            R = int(R)
            break

    write_pairings_to_file(tournament, R)


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
                "5": "Zwischenstand und Paarungen als Textdatei exportieren",
                "6": "Programm beenden"
           }

    print("\n"*5)
    print("===========================")
    print("=== CARL-FRIEDRICH V1.0 ===")
    print("===========================")
    print("Andreas Janzen, April 2021\n")

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
                current_tournament = enter_results(current_tournament)
            elif choice == "4":
                print_standings_menu(current_tournament)
            elif choice == "5":
                export_pairings(current_tournament)
            elif choice == "6":
                sys.exit()
        break # Leave input loop if user entered a valid choice


def main():
    while True:
        main_menu()


if __name__ == "__main__":
    main()

