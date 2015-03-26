#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname='tournament'")

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """ 
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT insert_Players(%s)",(name,))
    conectdb.commit()
    cursor.close()
    conectdb.close()

def deleteMatches():
    """Remove all the match records from the database."""
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT delete_Matches();")
    conectdb.commit()
    cursor.close()
    conectdb.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT delete_Players();")
    conectdb.commit()
    cursor.close()
    conectdb.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT * FROM number_players;")
    number_players = cursor.fetchone()
    conectdb.commit()
    cursor.close()
    conectdb.close()
    return number_players[0]


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
    cursor.execute("SELECT * from player_standings;")
    list_player = cursor.fetchall()
    conectdb.commit()
    cursor.close()
    conectdb.close()
    return list_player
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conectdb = connect()
    cursor = conectdb.cursor()
    cursor.execute("SELECT report_match(%s,%s)",(winner,loser))
    conectdb.commit()
    cursor.close()
    conectdb.close()  
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
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

'''deletePlayers()
deleteMatches()
registerPlayer('Joel')
registerPlayer('Fabian')
registerPlayer('Gustavo')
registerPlayer('William')
registerPlayer('Moyeturo')
registerPlayer('Raul')
registerPlayer('Josue')
registerPlayer('Jonatan')'''
print countPlayers()
reportMatch(124,125)
reportMatch(126,127)
reportMatch(128,129)
print playerStandings()