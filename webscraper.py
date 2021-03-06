#!/usr/bin/env python3
"""
=============
webscraper.py
=============

Author : Dr. Andreas Janzen
Email  : janzen (at) gmx.net
Date   : 2021-04-07
Version: 1.0

Provides methods to create a player list for a chess tournament. Player data
can either be fetched from the rating database of Deutscher Schachbund, or
they can be entered manually. Data for a single player is passed as a
dictionary, for groups of players, a list of dictionaries is passed between
functions.

Data fields in the dictionary comprise 'name', 'DWZ', 'evals' (number of DWZ
evaluations), 'ELO' and 'club' (can be used for affiliation in general, e.g.
for country, club, etc.).

Functions in webscraper.py:
===========================
get_players_by_name(name)
    Accepts a string as input parameter, then calls the rating website of the 
    German Chess Association (Deutscher Schachbund, DSB) for that name and
    returns a list of dictionaries with the players that matched the name.

print_player_list(player_list)
    Prints the list "player_list" in a structured form. Always returns None.

enter_player_data()
    Lets the user enter the player data manually and returns a dict with the
    same entries as if the data had been retrieved from the online database.

chose_player()
    Lets the user enter a player name, then calls get_players_by_name to fetch
    the results from the DSB database. Finally, lets the user chose one of the
    hits or enter the data manually. Returns a dict with the player details.

create_player_list(number_players)
    Creates a list of players by calling chose_player "number_players" times.
    Returns a list of dictionaries with player details. Adds a bye, "spielfrei"
    if "number_players" is odd.

main()
    Just a placeholder, does nothing.
"""


import pandas as pd


# Global variable for German Chess Association's rating databases
DB_DSB = "https://www.schachbund.de/spieler.html?search="


def get_players_by_name(name):
    """Accepts a name (last, first) as input and retrieves corresponding player
    details from the rating list of Deutscher Schachbund. Converts the scraped
    HTML table into a list of dictionaries with entries for name (from
    database), DWZ, evals (number of DWZ evaluations), ELO and club.
    """
    URL = DB_DSB + "%2C".join([s.strip() for s in name.split(",")])

    results = list()

    try:
        html = pd.read_html(URL)
    except Exception as e:
        print(f"\n\nERROR beim Laden von Daten aus der DSB-Datenbank:\n{e}\n\n")
        return results # results is an empty list at this point

    for i in range(len(html[1])):
        player = dict()

        try:
            player["name"] = html[1]["Spielername"][i]
            tmp = html[1]["DWZ"][i]
            if not pd.isna(tmp) and tmp != "Restp.":
                player["DWZ"] = int(tmp.split("-")[0])
                player["evals"] = int(tmp.split("-")[1])
            tmp = html[1]["Elo"][i]
            if tmp != "-----":
                player["ELO"] = int(tmp)
            player["club"] = html[1]["Verein"][i]
        except Exception as e:
            print("\n\nERROR!\nWebseite kann nicht gelesen werden! Bitte",
                  f"kontaktieren Sie den Autor der Software!\n{e}\n\n")

        results.append(player)

    return results


def print_player_list(player_list):
    """Takes a list of dictionaries as input parameter player_list, then
    traverses the list and prints the player details in structured form,
    similar to the DWZ website of Deutscher Schachbund.
    """
    for index, player in enumerate(player_list, 1):
        if player['name'] == "spielfrei":
            continue
        try:
            print(f"{index:2d}. {player['name'][:25]:25s}, ", end="")
            if player.get("DWZ", ""):
                print(f"DWZ {player['DWZ']:4d}", end="")
                if player.get("evals", ""):
                    print(f"-{player['evals']:3d}, ", end="")
                else:
                    print("," + " "*5, end="")
            else:
                print(" "*14, end="")
            if player.get("ELO", ""):
                print(f"ELO {player['ELO']:4d}, ", end="")
            else:
                print(" "*10, end="")
            if player.get("club", ""):
                print(f"{player['club'][:25]:25s}")
            else:
                print()
        except Exception as e:
            print("\n\nERROR!\nDas Datenformat stimmt nicht mit dem",
                  f"erwarteten Format ??berein!\n{e}\n\n")

    return None


def enter_player_data():
    """Allows to enter the same data that is fetched from the ratings database
    of Deutscher Schachbund to be added manually. Converts the input data into
    a dictionary that is returned from the function. DWZ, evals and ELO and
    converted to int values.
    """
    while True:
        print("\n\n---------------------")
        print("Manuelle Dateneingabe")
        print("---------------------")
        print("\nAngaben, die nicht zwingend gemacht werden muessen, sind",
                "durch '(opt.)' gekennzeichnet.")
        print("Die Dateneingaben kann mit ENTER uebersprungen werden.\n")

        last_name = input("Nachname" + "."*21 + " > ")
        first_name = input("Vorname (opt.)" + "."*15 + " > ")

        DWZ = input("DWZ (opt.)" + "."*19 + " > ")
        if DWZ != "" and DWZ.isnumeric():
            DWZ = int(DWZ)
        else:
            DWZ = 0
        evals = input("Anzahl Auswertungen (opt.)... > ")
        if evals != "" and evals.isnumeric():
            evals = int(evals)
        else:
            evals = 0
        ELO = input("ELO (opt.)" + "."*19 + " > ")
        if ELO != "" and ELO.isnumeric():
            ELO = int(ELO)
        else:
            ELO = 0
        club = input("Verein, Land, etc. (opt.).... > ")

        if last_name:
            player = {}
            player["name"] = ",".join([last_name, first_name]) \
                if first_name else last_name
            if DWZ != 0:
                player["DWZ"] = DWZ
            if evals != 0:
                player["evals"] = evals
            if ELO != 0:
                player["ELO"] = ELO
            if club:
                player["club"] = club

            return player
        else:
            return None


def chose_player():
    """Asks the user for a player name, fetches the database output for that
    name, prints the list of potential players and lets the user chose one of
    them, or -- if the sought player is not in the list -- lets the user chose
    to enter the player details manually.

    Returns a dict with the details for the chosen or manually entered player.
    """
    while True:
        name = input("Spieler (Nachname[, Vorname]): ")
        if name:
            break
    results = get_players_by_name(name)
    print_player_list(results)
    while True:
        print("\nBitte waehlen Sie einen Spieler aus der folgenden Liste.")
        print("Wenn Sie die Spielerdaten manuell eingeben moechten, geben Sie",
              "bitte eine 0 ein.")
        choice = input("> ")
        if choice.isnumeric():
            chosen = int(choice)
            if chosen == 0:
                manual_entry = enter_player_data()
                return manual_entry
            else:
                return results[chosen-1]


def create_player_list(number_players):
    """Create a list of players according to the input parameter number_players
    by repeated call to chose player. The function returns a list of
    dictionaries, each of which contains the details for one of the chosen
    players. If the number of players is an odd number, a bye ("spielfrei") is
    added as the last player to make the number of players even.
    """
    player_list = list()
    tmp_str = f"Eingabe der Teilnehmerliste mit {number_players} Spielern"
    print("\n\n" + "=" * len(tmp_str))
    print(tmp_str)
    print("=" * len(tmp_str))

    for i in range(1, number_players+1):
        tmp_str = f"Auswahl Spieler {i}/{number_players}"
        print("\n" + "-" * len(tmp_str))
        print(tmp_str)
        print("-" * len(tmp_str))
        # Make sure that details are provided for every player, otherwise
        # repeat the chosing process
        while True:
            new_player = chose_player()
            if new_player:
                player_list.append(new_player)
                break

    # Add a player as a bye to get an even number of players
    if number_players % 2 != 0:
        player_list.append({"name": "spielfrei"})


    return player_list


def main():
    """docstring
    """
    pass


if __name__ == "__main__":
    main()
