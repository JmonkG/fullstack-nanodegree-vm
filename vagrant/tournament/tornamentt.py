#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    return cur

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """ 
    conn = psycopg2.connect("dbname='tournament'")
    cur = conn.cursor()
    cur.execute("SELECT insert_Players(%s)",(name,))
    cur.execute("SELECT * FROM Players;")
    lis =  cur.fetchall()
    print lis

registerPlayer('Mariloli')
