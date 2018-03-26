Before running this web app, build the sqlite3 database from the ASCII dump file.
(The database file is binary, so the ASCII file is better for version control).
This is done by typing:
$ sqlite3 UNRESPWeb.db < UNRESPWeb.sql

Similarly, to update the dump file before committing to the git repo, type:
$ sqlite3 UNRESPWeb.db .dump > UNRESPWeb.sql

To run the app locally, simply type:
$ python3 app.py
open up a web browser and navigate to the appropriate URL/IP address.
This will typically be localhost:5000.
If running on foe-linux, source the appropriate modules first:
$ module load python3 python-libs

Note that in order for the app to run successfully, the file AppSecretKey.txt must be in the app's root directory.
This file is not version-controlled.