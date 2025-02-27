CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE user_connections (
    user1_id INT REFERENCES users(id) ON DELETE CASCADE,
    user2_id INT REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (user1_id, user2_id),
    CHECK (user1_id < user2_id)
);
