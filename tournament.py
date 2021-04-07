#!/usr/bin/env python3
"""
=============
tournament.py
=============

Dr. Andreas Janzen, janzen@gmx.net
Version 0.1, 2021-04-05
"""


from webscraper import create_player_list, print_player_list


def get_tournament_details():
    """Ask user for details of a newly created tournament:name, number of
    players, and tournament venue
    Returns a dictionary with the respective fields plus lists for all rounds,
    including the pairings in the form of player numbers and lists with the
    results of each round.
    """
    tournament = dict()

    print("\nLege ein neues Rundenturnier an...\n")

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

    return tournament


def create_new_pairings(R, old_positions):
    """docstring
    """
    n = len(old_positions)

    # R: number of new round, old_positions: positions of round R-1
    new_positions = list(old_positions)

    # Player n always stays at his position.
    new_positions[n-1] = n
    new_positions[:(int(n/2.)-1)] = old_positions[int(n/2.):(n-1)]
    new_positions[(int(n/2.)-1):(n-1)] = old_positions[:int(n/2.)]

    # Return positions without considering if player n has to flip the board,
    # since the next pairings will be calculated without (!) consideration of
    # whether player n had to rotate the board.
    return new_positions


def return_pairings(R, positions):
    """docstring
    """
    n = len(positions)
    pairings = list()

    # If R is an even round, player 10 has to switch colors with his opponent
    if R % 2 == 0:
        pairings.append([positions[n-1], positions[0]])
    else:
        pairings.append([positions[0], positions[n-1]])

    for table in range(1, int(n/2.)):
        pairings.append([positions[table], positions[n-table-1]])

    # Return pairings as a string with colours for player n potentially swapped
    return pairings


def print_pairings(pairings, player_list):
    for pairing in pairings:
        player1 = pairing[0]
        player2 = pairing[1]
        white = player_list[player1-1]['name']
        black = player_list[player2-1]['name']
        print(f"{white:20s} - {black:20s}")
    print("\n")



def main_menu():
    """Main menu
    """
    print("\n\n==================")
    print("=== Hauptmenue ===")
    print("==================\n")

    print("")


def main():
    """docstring
    """
    print("\n\n===========================")
    print("=== CARL-FRIEDRICH V1.0 ===")
    print("===========================")
    print("\nAndreas Janzen, 2021-04-05\n\n")

    tournament = get_tournament_details()
    player_list = create_player_list(tournament["players"])

    tmp_str = f"Teilnehmerliste {tournament['name']}"
    print("\n\n" + "=" * len(tmp_str))
    print(tmp_str)
    print("=" * len(tmp_str))
    print_player_list(player_list)
    print("\n\n")

    if len(player_list) % 2 != 0:
        player_append({'name': 'spielfrei'})

    positions = list(range(1, len(player_list)+1))

    pairings = return_pairings(1, positions)
    print(f"Paarungen Runde 1:")
    print("------------------")
    print_pairings(pairings, player_list)

    for R in range(2, len(player_list)):
        positions = create_new_pairings(R, positions)
        pairings = return_pairings(R, positions)
        print(f"Paarungen Runde {R}:")
        print("------------------")
        print_pairings(pairings, player_list)

    print("\n\nTschuess!\n")


if __name__ == "__main__":
    main()
