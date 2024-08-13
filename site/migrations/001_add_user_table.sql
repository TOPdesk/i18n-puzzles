CREATE TABLE users (
        id INTEGER NOT NULL, 
        external_id VARCHAR(64) NOT NULL, 
        username VARCHAR(64) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (external_id)
);

ALTER TABLE score ADD COLUMN user_id INTEGER DEFAULT NULL REFERENCES users (id);

INSERT INTO users (username, external_id) select distinct player_name, 'dummy:' || player_name from score;

UPDATE score SET user_id = (SELECT id FROM users where username = score.player_name);
