Before running this web app, build the sqlite3 database from the ASCII dump file.
(The database file is binary, so the ASCII file is better for version control).
This is done by typing:
$ sqlite3 UNRESPWeb.db < UNRESPWeb.sql

Similarly, to update the dump file before committing to the git repo, type:
$ sqlite3 UNRESPWeb.db .dump > UNRESPWeb.sql

To run the app in development mode (on localhost), do the following:
- In UNRESPWebApp.py, change the subdomain variable (subd) from "/vumo-data" to ""
- In UNRESPWebApp.py, add "debug=True" inside the parentheses in the call to app.run
- If on the FOE system, load the appropriate python modules: $ module load python3 python-libs
- Run the application by typing: $ python3 UNRESPWebApp.py
- Open up a web browser and navigate to localhost:5000
Don't forget to reset subd and remove debug mode before committing to github (production mode)

Note that in order for the app to run successfully, the file AppSecretKey.txt must be in the app's root directory.
This file is not version-controlled.

To make any code changes take effect on the server, type:
$ sudo systemctl restart httpd
