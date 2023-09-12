

DROP TABLE IF EXISTS user_tabl;
DROP TABLE IF EXISTS admin_tabl;
DROP TABLE IF EXISTS item_details;


CREATE TABLE user_tabl (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE Admin_tabl (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE item_details (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    image_path VARCHAR(255) NOT NULL
);
-- Insert users into the table
INSERT INTO user_tabl (username, password)
VALUES('johnDoe', 'password1'),
      ('JaneSmith', 'password2'),
      ('AliceJohnson','password3');

SELECT*
FROM user_tabl;      