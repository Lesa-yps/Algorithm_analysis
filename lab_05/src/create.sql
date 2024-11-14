-- CREATE DATABASE DB_Recipies;

DROP TABLE IF EXISTS Steps CASCADE;
DROP TABLE IF EXISTS Ingredients CASCADE;
DROP TABLE IF EXISTS Recipes CASCADE;

CREATE TABLE IF NOT EXISTS Recipes (
    id INT PRIMARY KEY,
    issue_id INT,
    url TEXT,
    title TEXT,
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS Ingredients (
    id SERIAL PRIMARY KEY,
    rec_id INT,
    title TEXT,
    count TEXT,
    FOREIGN KEY (rec_id) REFERENCES Recipes (id)
);

CREATE TABLE IF NOT EXISTS Steps (
    id SERIAL PRIMARY KEY,
    rec_id INT,
    step TEXT,
    step_num INT,
    FOREIGN KEY (rec_id) REFERENCES Recipes (id)
);