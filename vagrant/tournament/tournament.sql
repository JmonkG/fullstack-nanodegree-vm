-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE  tournament;

CREATE TABLE Players(PlayerID SERIAL PRIMARY KEY,FirstName varchar(255),Wins int,Matches int);

CREATE TABLE Matches( MatchID SERIAL PRIMARY KEY, Winner int,Loser int);

CREATE VIEW number_players AS SELECT COUNT(*) FROM Players;
CREATE VIEW list_players AS SELECT PlayerID,FirstName,Wins from Players order by Wins ASC;

CREATE FUNCTION delete_Players() RETURNS void  AS $$DELETE FROM Players;$$ LANGUAGE SQL;

CREATE FUNCTION delete_Matches() RETURNS void AS $$ DELETE FROM Matches;$$ LANGUAGE SQL;

CREATE FUNCTION insert_Players(name varchar(30)) returns void AS $$  INSERT INTO Players(FirstName,Wins,Matches) VALUES (name,0,0); $$ LANGUAGE SQL;

CREATE FUNCTION return_Players(out id int,out name varchar(30),out win int,out los int) RETURNS SETOF record AS $$
SELECT * from Players ORDER BY Wins DESC;
$$ LANGUAGE SQL;


CREATE FUNCTION report_match(in winner int,in loser int) RETURNS VOID AS $$
INSERT INTO Matches(Winner,Loser) VALUES (Winner,Loser);
UPDATE Players set Wins = Wins + 1 WHERE PlayerID = Winner;
UPDATE Players set Matches = Matches + 1 WHERE PlayerID = Winner OR PlayerID = Loser;
$$ LANGUAGE SQL;