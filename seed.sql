-- Create table for football teams
CREATE TABLE team (
    id SERIAL PRIMARY KEY,
    name TEXT NOT null
    );


-- Create table for game
CREATE TABLE game (
    id INT PRIMARY KEY,
    home_team_id INT REFERENCES team(id), -- home team for game
    away_team_id INT REFERENCES team(id) -- away team for game
    );

-- Create table for game result
CREATE TABLE game_result (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES game(id),
    team_id INT REFERENCES team(id),
    points INT NOT NULL, -- points the team scored
    is_winner BOOLEAN, -- boolean that indicates if the team won
    CONSTRAINT unique_game_team UNIQUE (game_id, team_id)
    );

-- Sample data for team
INSERT INTO team (id, name) VALUES
(1, 'Washington Huskies'),
(2, 'Boise State'),
(3, 'Tulsa Golden Hurricane'),
(4, 'Michigan State Spartans'),
(5, 'California Golden Bears'),
(6, 'Arizona Wildcats'),
(7, 'Oregon Ducks'),
(8, 'Arizona State Sun Devils'),
(9, 'Stanford Cardinal'),
(10, 'USC Trojans'),
(11, 'Utah Utes'),
(12, 'Oregon State Beavers'),
(13, 'Washington State Cougars'),
(14, 'Texas Longhorns'),
(15, 'Michigan Wolverines');

-- Sample data for game
INSERT INTO game (id, home_team_id, away_team_id) VALUES
(1, 1, 2), -- Boise State | Home | 56-19
(2, 1, 3), -- Tulsa | Home | 43-10
(3, 4, 1), -- Michigan State | Away | 41-7
(4, 1, 5), -- California | Home | 59-23
(5, 6, 1), -- Arizona | Away | 31-24
(6, 1, 7), -- Oregon | Home | 36-33
(7, 1, 8), -- Arizona State | Home | 15-7
(8, 9, 1), -- Stanford | Away | 42-33
(9, 10, 1), -- USC | Away | 52-42
(10, 1, 11), -- Utah | Home | 35-28
(11, 12, 1), -- Oregon State | Away | 22-20
(12, 1, 13), -- Washington State | Home | 24-21
(13, 1, 7), -- Oregon | Home | 34-21
(14, 1, 14), -- Texas | Home | 37-31
(15, 15, 1); -- Michigan | Away | 13-34

-- Sample data for game results
INSERT INTO game_result (game_id, team_id, points, is_winner) VALUES
(1, 1, 56, TRUE),
(1, 2, 19, FALSE),
(2, 1, 43, TRUE),
(2, 3, 10, FALSE),
(3, 1, 41, TRUE),
(3, 4, 7, FALSE),
(4, 1, 59, TRUE),
(4, 5, 23, FALSE),
(5, 1, 31, TRUE),
(5, 6, 24, FALSE),
(6, 1, 36, TRUE),
(6, 7, 33, FALSE),
(7, 1, 15, TRUE),
(7, 8, 7, FALSE),
(8, 1, 42, TRUE),
(8, 9, 33, FALSE),
(9, 1, 52, TRUE),
(9, 10, 42, FALSE),
(10, 1, 35, TRUE),
(10, 11, 28, FALSE),
(11, 1, 22, TRUE),
(11, 12, 20, FALSE),
(12, 1, 24, TRUE),
(12, 13, 21, FALSE),
(13, 1, 34, TRUE),
(13, 7, 21, FALSE),
(14, 1, 37, TRUE),
(14, 14, 31, FALSE),
(15, 15, 34, TRUE),
(15, 1, 13, FALSE);

