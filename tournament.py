#!/usr/bin/env python3
"""
=============
tournament.py
=============

Author : Dr. Andreas Janzen
Email  : janzen (at) gmx.net
Date   : 2021-04-07
Version: 1.0

Implements functions to organize a round-robin chess tournament:
    - Create the tournament and store the key data in a dictionary
    - Create a list of pairings, dependent on the number of players
    - Print the pairing list for a certain round
    - Get results for individual games and calculate the new ranking table

Data structure:
    Dictionary 'tournament' contains key data (name, number of players and
    rounds, venue, date of last round), player list (supplemented by an
    additional player to manage byes, if odd) with fixed order (index used for
    abbreviation of pairing tables and standings), pairings for each round as a
    list of lists containing the indices of the players at the given virtual
    table and the result of the game. Results are abbreviated with a single
    character, which is translated into points gained by both players with a
    dictionary RESULTS2POINTS. standings is a list that contains a dictionary
    with the player indices as keys and the achieved points as values. The
    ranking can then easily be deduced by sorting that list by values and
    finding the player name for each player index.
"""


from datastorage import write_tournament_data, read_tournament_data, \
                        get_tournament_filename, switch_stdout
from webscraper import create_player_list, print_player_list


EXPAND_RESULT = {
        "1": "1 - 0",
        "0": "0 - 1",
        "=": "= - =",
        "+": "+ - -",
        "-": "- - +",
        "C": "- - -",
        "_": ""
        }

RESULT2POINTS = {
        "1": [1, 0],     # White wins
        "=": [0.5, 0.5], # Draw
        "0": [0, 1],     # Black wins
        "+": [1, 0],     # Bye for white
        "-": [0, 1],     # Bye for black
        "C": [0, 0],     # Game has been cancelled
        "_": [0,0]       # No result yet
        }


def create_new_tournament():
    """Ask user for details of a newly created tournament: name, number of
    players, and tournament venue

    Returns a dictionary with the respective fields plus lists for all rounds,
    including the pairings in the form of player numbers and lists with the
    results of each round.
    """
    tournament = dict()

    print("\n\nNeues Rundenturnier anlegen")
    print("===========================\n")

    while True:
        tournament_name = input("Turnierbezeichnung > ").strip()
        if tournament_name:
            tournament["name"] = tournament_name
            break
    while True:
        tournament_players = input("Teilnehmerzahl.... > ").strip()
        if tournament_players.isnumeric():
            tournament["players"] = int(tournament_players)
            break
    while True:
        tournament_venue = input("Spielort.......... > ").strip()
        if tournament_venue:
            tournament["venue"] = tournament_venue
            break

    # create_player_list adds an additional player (a bye) to the player list
    # to make the number of players an even number. The "players" entry in the
    # dictionary remains unchanged. It counts only the real players.
    tournament["player_list"] = create_player_list(tournament["players"])
    tournament["rounds"] = create_pairing_list(len(tournament["player_list"]))
    tournament["standings"] = list([0]*len(tournament["player_list"]))

    write_tournament_data(tournament)

    return tournament


def load_tournament():
    """Load tournament data from json file. Files are stored in folder ./data.
    Player list is printed to show that the data have been loaded successfully.
    Can be removed in a future update.
    """
    filename = get_tournament_filename()
    tournament = read_tournament_data(filename)

    tmp_str = "Teilnehmerliste " + tournament["name"]
    print("\n\n" + tmp_str)
    print("=" * len(tmp_str))
    print_player_list(tournament["player_list"])

    return tournament


def create_new_round(old_positions):
    """Create new table positions based on scheme described in Wikipedia
    article on round robin system (Berger tables). For each new round, player n
    stays at his position if the number of players is even, while all other
    players rotate counte-clockwise by n/2 positions. If the number of players
    is odd, an additional n+1-th players is added as a bye. His opponent always
    wins.

    In every other round, player n has to rotate his board to get alternating
    colours. The list "positions" is returned without considering if player n
    has to flip the board, since the next pairings will be calculated without
    consideration of whether player n had to rotate the board.
    """
    # n: number of players, old_positions: positions of previous round
    n = len(old_positions)
    new_positions = list(old_positions)

    # Player n always stays at his position.
    new_positions[n-1] = n
    # Rotate positions 1...n-1 by 5 positions counter-clockwise
    new_positions[:(int(n/2.)-1)] = old_positions[int(n/2.):(n-1)]
    new_positions[(int(n/2.)-1):(n-1)] = old_positions[:int(n/2.)]

    return new_positions


def return_pairings(R, positions):
    """ Return pairings as a list of pairings with colours for player n
    swapped in every other round to give him alternating colours. "_" is added
    to each pairing as a placeholder for the result and an indicator that the
    game has not been played yet (see conversion dictionary RESULT2POINTS).
    """
    n = len(positions)
    pairings = list()

    # If R is an even round, player n has to switch colors with his opponent
    if R % 2 == 0:
        pairings.append([positions[n-1], positions[0], "_"])
    else:
        pairings.append([positions[0], positions[n-1], "_"])

    for table in range(1, int(n/2.)):
        pairings.append([positions[table], positions[n-table-1], "_"])

    return pairings


def create_pairing_list(number_players):
    """Returns a list with pairings for each round of the tournaments the
    pairings are triples of two player indices and a character that indicates
    the outcome of a game according to the conversion dictionary RESULT2POINTS.

    number_players corresponds to the number of real players plus a bye if the
    number of players is an odd number. This bye is always the player with the
    highest index in the player list.

    Positions and pairings are kept separately because the colours at the board
    where player n plays are swapped every other round.
    """
    pairing_list = list()

    # Round 1: players are sorted in order, from then on use shifting scheme
    R = 1
    positions = list(range(1, number_players+1))

    # For all rounds: add pairing list to local variable, then increase R for
    # next round and rotate player positions
    while R <= number_players - 1:
        pairing_list.append(return_pairings(R, positions))
        positions = create_new_round(positions)
        R += 1

    return pairing_list


def print_pairings(tournament, R):
    """docstring
    """
    pairing_list = tournament["rounds"][R-1]

    for pairing in pairing_list:
        white = tournament["player_list"][pairing[0]-1]["name"][:25]
        black = tournament["player_list"][pairing[1]-1]["name"][:25]
        result = EXPAND_RESULT[pairing[2]]

        print(f"{white:25s} - {black:25s}  {result}")
    print()

    return None


def update_result(tournament, R, game, result):
    """Change the result of a game in a tournament. R designates the round,
    game the game number, but they need to be converted to 0-based indices! The
    resulting tournament standing is written to the json file after
    confirmation from the user.
    """
    # Update the tournament results and standings
    tournament["rounds"][R-1][game-1][2] = result

    # Ask for confirmation and save the new tournament dictionary or discard.
    tmp_str = f"Aktualisierte Resultate in Runde {R}:"
    print("\n" + tmp_str)
    print("-" * len(tmp_str))
    print_pairings(tournament, R)

    write_tournament_data(tournament)

    return tournament


def refresh_scores(tournament, R):
    """docstring
    """
    if not tournament:
        print("\n\n*** No tournament data available! ***\n\n")
        return

    # Reset score count to 0
    tournament["standings"] = list([0] * len(tournament["player_list"]))

    # Calculate scores from all rounds up to round R
    for round in tournament["rounds"][:R]:
        for game in round:
            # Get the player ids for white and black (1...number of players)
            # Using player indices as list indices then requires to subtract 1!
            white = game[0]
            black = game[1]
            result = game[2]

            if result == "1" or result == "+":
                tournament["standings"][white-1] += 1
            elif result == "0" or result == "-":
                tournament["standings"][black-1] += 1
            elif result == "=":
                tournament["standings"][white-1] += 0.5
                tournament["standings"][black-1] += 0.5
            elif result == "C" or result == "_":
                pass

    return tournament


def print_standings(tournament, R):
    """docstring
    """
    # Create a sorted list of player indices (0-based) corresponding to the
    # sorted order of the scores in the tournament entry called "standings"
    scores = tournament["standings"]
    ranking = sorted(range(len(scores)), key = lambda k: scores[k], \
            reverse = True)

    tmp_str = f"Stand nach Runde {R}:"
    print("\n" + tmp_str)
    print("=" * len(tmp_str))

    for rank, player_index in enumerate(ranking, 1):
        player_name = tournament['player_list'][player_index]['name']
        player_rating = tournament['player_list'][player_index].get('DWZ',"")
        player_score = tournament["standings"][player_index]

        if player_name == "spielfrei":
            continue

        print(f"{rank:2d}. {player_name:25s}",
              f"{(', ' + str(player_rating)) if player_rating else ' '*6}, ",
              f"{player_score} Punkte")

    return None


def write_pairings_to_file(tournament, R):
    """docstring
    """
    filename = tournament["name"].replace(" ", "_") + f"_R{R}" + ".txt"

    # Switch standard output to file, the use existing functions to output data
    try:
        switch_stdout(filename)
    except Error as e:
        print("\n\n*** Kann nicht in Datei exportieren! ***\n\n")
        return None

    tmp_str = "CARL-FRIEDRICH V1.0"
    print("=" * (len(tmp_str) + 8))
    print("=== " + tmp_str + " ===")
    print("=" * (len(tmp_str) + 8) + "\n")

    tmp_str = f"Zwischenstand und Paarungsliste für Runde {R}:"
    print(tmp_str)
    print("-" * len(tmp_str))

    refresh_scores(tournament, R-1)
    print_standings(tournament, R-1)

    tmp_str = f"Paarungen in Runde {R}:"
    print("\n" + tmp_str)
    print("=" * len(tmp_str))

    print_pairings(tournament, R)

    # Switch standard output back to console
    switch_stdout()

    return None


def main():
    """docstring
    """
    pass


if __name__ == "__main__":
    main()
