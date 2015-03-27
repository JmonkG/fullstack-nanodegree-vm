-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
BEGIN;    

-- Each Player has 4 fields: ID,FirstName,number of wins (Wins) and number of matches played (Matches)
CREATE TABLE Players(PlayerID SERIAL PRIMARY KEY,FirstName varchar(255),Wins int,Matches int);

-- Each Match has 3 fields: it's ID as primary key and 2 foreign keys from the IDs of the Players in the Match
CREATE TABLE Matches( MatchID SERIAL PRIMARY KEY, Winner int references Players(PlayerID),Loser int references Players(PlayerID));

-- view that returns the number of players on the table PLayers
CREATE VIEW number_players AS SELECT COUNT(*) FROM Players;

-- view that returns a list of players ordered in based of their winnings. The players with most winnings come first.
CREATE VIEW player_standings AS SELECT PlayerID,FirstName,Wins,Matches from Players order by Wins DESC;

-- view that returns a list of players ordered in reverse as player_standings. This is in order to ease the process of create the pairs :)
CREATE VIEW swiss_pairs AS SELECT PlayerID,FirstName from Players order by Wins ASC;

-- function that deletes all the players in table Players
CREATE FUNCTION delete_Players() RETURNS void  AS $$DELETE FROM Players;$$ LANGUAGE SQL;

-- function that deletes all the matches in table Matches
CREATE FUNCTION delete_Matches() RETURNS void AS $$ DELETE FROM Matches;$$ LANGUAGE SQL;

-- function that inserts a new player in the Players Table. It takes just the name and initializes its Wins and MAtches to 0 .
CREATE FUNCTION insert_Players(name varchar(30)) returns void AS $$  INSERT INTO Players(FirstName,Wins,Matches) VALUES (name,0,0); $$ LANGUAGE SQL;

-- function that creates a match in table Matches with a determined winner. At the same time, updates the Wins and Matches fields in the correspondent players
CREATE FUNCTION report_match(in winner int,in loser int) RETURNS VOID AS $$
INSERT INTO Matches(Winner,Loser) VALUES (Winner,Loser);
UPDATE Players set Wins = Wins + 1 WHERE PlayerID = Winner;
UPDATE Players set Matches = Matches + 1 WHERE PlayerID = Winner OR PlayerID = Loser;
$$ LANGUAGE SQL;

-- function that creates a match in table Matches when there is a tie. Only the field matches in both players is updated
CREATE FUNCTION report_match_tie(in player1 int,in player2 int) RETURNS VOID AS $$
INSERT INTO Matches(Winner,Loser) VALUES (player1,player2);
UPDATE Players set Matches = Matches + 1 WHERE PlayerID = player1 OR PlayerID = player2;
$$ LANGUAGE SQL;

END;
