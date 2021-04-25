#!/usr/bin/env python3

"""
carl-friedrich.py

Autor: Dr. Andreas Janzen
Email: janzen (at) gmx.net
Date : 2021-04-07

A command line app to organize round-robin chess tournaments

Player details can be loaded from the website of the German Chess Association,
pairings will be set according to the Berger tables that the FIDE recommends.
Data is stored locally in the form of json files. Intermediate standings and
pairings for the next round can be exported as ASCII text documents.

This is the main file of the application. Further modules are:
    - datastorage.py
    - tournament.py
    - webscraping.py

Functions in carl-friedrich.py:
===============================
enter_results(tournament)
    Lets the user chose a round and a game for which the result can be edited.
    Updates the tournament data and returns them as a dictionary to the calling
    function.

print_standings_menu(tournament)
    Lets the user enter a round, calculates the scores of all players after
    that round and displays the intermediate standings after that round. Always
    returns None.

export_pairings(tournament)
    Lets the user chose a round, then writes the intermediate standings
    before that round and the pairings of the round into an ASCII text file.

main_menu()
    Prints the main menu and lets the user chose a menu item.

main()
    Calls "main_menu" in an infinite loop. The user can quit the program in the
    main menu by call to sys.exit().
"""


import sys

from tournament import create_new_tournament, load_tournament, print_pairings,\
        update_result, refresh_scores, print_standings, write_pairings_to_file


# Define global variable to hold the current tournament data
current_tournament = None


def enter_results(tournament):
    """Lets the user chose a round R, prints the pairings and lets the user
    chose a game to edit, then asks for the result of that game and updates the
    tournament data accordingly. Returns the updated tournament data.
    """
    if not tournament:
        print("\nBitte laden Sie zunächst ein Turnier, oder legen Sie ein neues"
              " Turnier an.")
    else:
        print("\nBitte waehlen Sie die Runde, für die Sie Ergebnisse eingeben",
              "möchten.")
        while True:
            R = input("\nRunde > ")
            if R.isnumeric():
                R = int(R)
                if 0 < R <= len(tournament["player_list"])-1:
                    break

        print()
        print_pairings(tournament, R)

        while True:
            print("Bitte waehlen Sie eine Partie, oder geben Sie eine 0 ein,"
                  "um zum\nHauptmenue zurueckzukehren.")
            game = input("\nPartie > ")
            if game.isnumeric():
                game = int(game)
                if 0 <= game <= len(tournament["player_list"])/2:
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
    """Lets the user chose a round after which the intermediate standings shall
    be displayed, calculates the scores of all players after that round and
    displays the standings, sorted by the number of scored points.
    """
    if not tournament:
        print("\nBitte laden Sie zunächst ein Turnier, oder legen Sie ein neues"
              " Turnier an.")
    else:
        tmp_str = "Tabelle anzeigen"
        print("\n"+tmp_str)
        print("=" * len(tmp_str))

        print("Bitte waehlen Sie eine Runde, nach der der Tabellenstand",
              "\nangezeigt werden soll.\n")
        while True:
            R = input("Runde > ")
            if R.isnumeric():
                R = int(R)
                if 0 < R <= len(tournament["player_list"])-1:
                    break

        tournament = refresh_scores(tournament, R)
        print_standings(tournament, R)

        return None


def export_pairings(tournament):
    """Lets the user chose a round, then writes the intermediate standings
    before that round and the pairings of the round into an ASCII text file.
    """
    tmp_str = "Exportiere Zwischenstand und Rundenpaarungen in Textdatei"
    print("\n\n" + tmp_str)
    print("=" * len(tmp_str))
    print("\nDie Paarungen welcher Runde sollen exportiert werden?\n")

    while True:
        R = input("Runde > ")
        if R.isnumeric():
            R = int(R)
            if 0 < R <= len(tournament["player_list"])-1:
                break

    error = write_pairings_to_file(tournament, R)

    if error == "OK":
        return None
    else:
        print("\n\nERROR: Beim Datenexport in eine Textdatei ist ein Fehler",
              f"aufgetreten.\n{error}\n\n")
        return None


def main_menu():
    """Prints the main menu and lets the user chose a menu item.
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
    """Calls the function main_menu in an infinite loop.
    """
    while True:
        main_menu()


if __name__ == "__main__":
    main()

