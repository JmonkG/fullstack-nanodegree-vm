Project # 2 : Tournament Planner
=============

This project is divided in 3 files:
tournament.sql      : Has the SQL code for creating the tables (Players,Matches) and its correspondent views and functions to create on the tournament database. 
tournament.py       : It's the API for accessing the data from the tables in database tournament. Every function access to the tables through its correspondent view or function
tournament_test.py  : It's the code provided for testing the functionality of the implemented functions on tournament.py

Notes: in order to achieve the extra credits, there were some modifications made on the tournament_test.py so it won't affect the desired behaviour of the present code.

The idea behind the implemented solution is to minimize the SQL information on the tournament file. That way, if the file is compromised, there is no information of the tables and keys available. That would make ir harder to  realize a proper sql inyection on the site.
To execute the code, run the .sql file on the database to create the tables, views and functions. Afer that, just run tournament_test.py