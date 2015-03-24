-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE  tournament;

CREATE TABLE Players(
    PlayerID int NOT NULL PRIMARY KEY,
    FirstName varchar(255),
    Wins int,
    Matches int,
);
CREATE TABLE Matches(
    MatchID int NOT NULL PRIMARY KEY,
    Player1ID int,
    PLayer2ID int,
    Winner int,
    Loser int,
);

CREATE VIEW number_players AS SELECT COUNT(*) FROM Players;
CREATE PROCEDURE delete_Players AS DELETE * FROM Players;
CREATE PROCEDURE delete_Matches AS DELETE * FROM Matches;
CREATE PROCEDURE insert_Players AS @FirstName nvarchar(30) = NULL, @LastName nvarchar(30) = NULL AS INSERT INTO Players(FirstName,LastName,Rating,Wins,Matches) VALUES (@FirstName,@LastName,0,0,0);
CREATE PROCEDURE return_PLayers AS SELECT * from Players ORDER BY Wins ASC , Matches DESC;
