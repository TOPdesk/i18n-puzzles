
-- Now that we've deprecated player_name, it's time to remove it.
-- Backward breaking changes coming up

ALTER TABLE score DROP column player_name;

-- SQLite doesn't support adding constraint, so the following will have to be done by copying the data to a new table...
-- ALTER TABLE users ADD CONSTRAINT user_id NOT NULL;

ALTER TABLE score RENAME TO score_bkup;

CREATE TABLE score (
        id INTEGER NOT NULL, 
        puzzle_id INTEGER NOT NULL, 
        timestamp DATETIME,
        user_id INTEGER NOT NULL REFERENCES users (id), 
        PRIMARY KEY (id)
);

INSERT INTO score (id, puzzle_id, timestamp, user_id) SELECT id, puzzle_id, timestamp, user_id FROM score_bkup;