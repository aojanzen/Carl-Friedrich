# Carl-Friedrich
#### Video Demo:  https://youtu.be/e3rOckyPz5
#### Description:
Carl-Friedrich is a command line application that allows users to organize
chess tournaments with a focus on tournaments in Germany since the
menu navigation is in German, and the data entry form uses web queries from the
player database of the German Chess Association (Deutscher Schachbund, DSB),
even though data can also be entered manually. The app uses the pairing scheme
that is proposed by the World Chess Association (FIDE), the Berger pairing
tables, which are determined following a procedure described on Wikipedia
(https://en.wikipedia.org/wiki/Round-robin_tournament).

In the first development stage, my final project for Harvard's CS50 course, the
tournament type will be limited to round-robin, leaving the popular, but more
complex Swiss tournament for later. Other languages than German could also be
added as a later improvement, provided that the project will be maintained and
used in the long run.

Tournaments require the following input data:
- Name and venue of the tournament,
- Number of players (determines the number of rounds),
- Date of the last round (minimum information, option: dates of all rounds),

The following information must be provided for each player:
- Full name (last and first)
and optionally:
- Rating(s): national rating (Deutsche Wertungszahl, DWZ), number of
  evaluations, international rating (ELO)
- Affiliation, such as team or country

#### Code organisation:
**carl-friedrich.py**: Main program with a main menu in an infinite loop and
some high-level functions

**database.py**: Stores information about tournament and players in a json file
and loads them back into the program.

**tournament.py**: Provides methods for the actual organisation of the
tournament, such as creation of a new tournament, creation of a pairing table,
entering game results, and an export of intermediate standings and pairings of
the next round into an ASCII text file.

**webscraper.py**: Get data from the open online database of the German Chess
Association (Deutscher Schachbund, DSB), chose a player from the scraped data
or enter the data manually, print the player list.
