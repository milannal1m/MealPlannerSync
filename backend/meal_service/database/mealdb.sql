CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    user_id UUID NOT NULL,
    planned_for TIMESTAMP
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    meal_id INT REFERENCES meals(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    amount TEXT
);
