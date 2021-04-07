# Carl-Friedrich
#### Video Demo:  <URL HERE>
#### Description:
Carl-Friedrich is a web app that allows users to organize a chess tournament,
to store the current state of the tournament in a database and to have the app
determine the pairings for a round-robin tournament.

When the tournament is created, the user can enter user data manually and it
is possible to use information that the app gets from internet databases, such
as the FIDE database or the DWZ rating database of the German Chess Association.

In the first step (final project for Harvard's CS50 course), the tournament
type will be limited to round robin, leaving the popular, but more complex
Swiss tournament for later. Likewise, the user interface will be in German.
Other languages can be added as a later improvement, provided that the project
will be maintained and used in the long run.

Tournaments require the following input data:
- Name of the tournament,
- Number of players (determines the number of rounds),
- Date of the last round (minimum information, option: dates of all rounds),
- Name, email address, and a password for the tournament organizer
- Name and email address of one or more referees, if applicable

The following information has to be provided for each individual player:
- Full name
- Year of birth (to help with identification and rating update)
- Nationality
- Rating(s): ELO, national rating(s), e.g. Deutsche Wertungszahl (DWZ)
- Optional: association(s), such as team or club
- Comments can be added, e.g. about disability, penalty or exclusion

#### Code organisation:
**carlfriedrich.py**: Main program, using the Flask-specific file structure

**database.py**: Stores information about tournament and players in a sqlite3
database, provides methods to create new tournaments and new rounds, etc.

**tournament.py**: Provides methods for the actual organisation of the
tournament

yourapplication.py
    /static
        style.css
    /templates
        layout.html
        index.html
        login.html
        ...