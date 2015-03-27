#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """ 
    conectdb = connect()
    cursor = conectdb.cursor()  # set a cursor in the connection
    cursor.execute("SELECT insert_Players(%s)",(name,)) #execute the SQL function insert Players(name). This avoids revealing SQL code of the database
    conectdb.commit() # commits the transaction
    
    # good practice to close the cursor and database conection
    cursor.close()
    conectdb.close()

def deleteMatches():
    """Remove all the match records from the database."""
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT delete_Matches();") # uses the SQL function delete_Matches()
    conectdb.commit()
    cursor.close()
    conectdb.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT delete_Players();") # uses the SQL function delete_Players()
    conectdb.commit()
    cursor.close()
    conectdb.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT * FROM number_players;") #uses the SQL view number_players, wich retrieves the number of rows in Players
    number_players = cursor.fetchone() # number_players saves the fetching of the cursor, in this case, just one row
    cursor.close()
    conectdb.close()
    return number_players[0] #from the tuple retrieved, takes its firs value, the integer that represents the count of players


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT * from player_standings;") # uses the SQL view player_standings
    list_player = cursor.fetchall() #retrieves all the rows in players order by wins
    cursor.close()
    conectdb.close()
    return list_player
    

def reportMatch(player1, player2,tie): 
    """Records the outcome of a single match between two players.

    Args:
      player1:  the id number of the player1
      player2:  the id number of the player2
      tie:      a boolean variable that determines if the match has a winner or is a tie.
                if tie is 0 then there is a winner, in this case is player 1, if tie is 1 then is a tie and nobody wins
    """
    conectdb = connect()
    cursor = conectdb.cursor()
    if tie == 0:
        cursor.execute("SELECT report_match(%s,%s)",(player1,player2)) # uses the SQL function report_match to insert a new match on Matches
    else:
        cursor.execute("SELECT report_match_tie(%s,%s)",(player1,player2)) 
    conectdb.commit()
    cursor.close()
    conectdb.close()  
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    tup =()
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    final_list_players = [] # the final list of tuples in the desired format
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT * from swiss_pairs;") # uses the SQL view swiss_pairs to retrieve the list of players in the desired order
    swiss_pairs = cursor.fetchall()  
    cursor.close()
    conectdb.close()
    while(len(swiss_pairs) != 0): #while the list swiss_pass has elements
        first_player = swiss_pairs.pop() #takes the first player 
        second_player = swiss_pairs.pop() #takes the second player
        new_tuple = (first_player[0],first_player[1],second_player[0],second_player[1]) #forms the new tuple to add to the final list
        final_list_players.append(new_tuple)
    return final_list_players;
