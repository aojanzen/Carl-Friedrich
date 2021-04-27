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

#### Use of libraries:
**json**: Originally, the app was intended to be a web app with a sqlite
database in the background to store all player and tournament information.
After giving the issueus some though, I have decided not to use a database
because the player ratings change with every tournament and therefore storing
them for later use does not make sense. They have to be fetched from the
official rating database every time anew. Round-robin tournaments are ususally
only used for a rather small number of players because they would otherwise
take a lot of rounds. This means that also the amount of data that has to be
stored for a tournament is rather small. Finally, compound Python datatypes,
such as lists of dicts, etc. are automatically converted into json by the json
library. This makes storing and reading of the tournament data very easy.
Lastly, json files have the advantage that they are plain ASCII text and thus
make fault finding during the programming phase easy and allow the user to
check and retrieve the stored information independent of Carl-Friedrich, if
necessary.

**pandas**: The read_html method makes it very easy to scrape tabulated data
from html pages. I had to find the right element in the returned list of Pandas
dataframes experimentally, but it was possible to get to the sought data in a
relatively short time. Online databases of other chess federations, e.g. the
USCF database, could be accessed in an identical fashion, as long as the URL
that is used to send the query to the webserver can be composed in a simple
way.

If the app should be translated to English in the future, the US Chess
Federation (USCF) has a database that works with queries in a similar way. The
minimal search string for a player named "John Smith" is

https://new.uschess.org/player-search?submit=1&display_name=Smith%252C%2520John

#### Next steps:
If the app should be improved in the future, the most important step to make it
widely usable is to refactor the code so that the functions that are used to
handle player data and tournament data, e.g. printing the intermediate
standings, are easier to reuse. The next big step would then be to change the
app so that one can organize either round-robin or Swiss tournaments. The
latter are much more complex, but they also have a real-world value because
Swiss tournaments are the type that is actually played a lot in real life.
Beyond that, the next valuable step is certainly to turn the app into a web app
so that the tournaments can be organized from a mobile phone rather than a PC
with Python installed. Translating the app into other languages and the
inclusion of other player databases are lower in priority. The app will hardly
be used in real life as long as Swiss tournaments cannot be handled.
