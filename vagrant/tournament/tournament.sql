-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE  tournament;

CREATE TABLE Players(PlayerID SERIAL PRIMARY KEY,FirstName varchar(255),Wins int,Matches int);

CREATE TABLE Matches(
    MatchID SERIAL PRIMARY KEY,
    Winner int,
    Loser int
);

CREATE VIEW number_players AS SELECT COUNT(*) FROM Players;
CREATE PROCEDURE delete_Players AS DELETE * FROM Players;
CREATE PROCEDURE delete_Matches AS DELETE * FROM Matches;
CREATE PROCEDURE insert_Players AS @FirstName nvarchar(30) = NULL AS INSERT INTO Players(FirstName,Wins,Matches) VALUES (@FirstName,0,0);
CREATE PROCEDURE return_PLayers AS SELECT * from Players ORDER BY Wins ASC , Matches DESC;
CREATE PROCEDURE report_match AS @winner int,@loser int
AS INSERT INTO Matches(Winner,Loser) VALUES (@winner,@loser)
AS UPDATE TABLE PLAYERS set Matches = Matches + 1 WHERE PlayerID = @winner OR PLAYERID =@loser ;
CREATE VIEW list_players AS SELECT PlayerID,FirstName,Wins from Players order by Wins ASC;
