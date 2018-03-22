Before running this web app, build the sqlite3 database from the ASCII dump file.
(This is done because the database file is binary, so the ASCII file is better for version control).
This is done by typing:
$ sqlite3 UNRESPWeb.db < UNRESPWeb.sql

Similarly, to update the dump file before committing to the git repo, type:
$ sqlite3 UNRESPWeb.db .dump > UNRESPWeb.sql

To run the app, simply type:
$ python3 app.py
open up a web browser and navigate to the appropriate URL/IP address.
This will typically be localhost:5000 if running locally.
