CREATE DATABASE pharma;

CREATE TABLE users
(
    user_id    INT GENERATED ALWAYS AS IDENTITY,
    username   varchar(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id)
);

CREATE TABLE products
(
    product_id        INT GENERATED ALWAYS AS IDENTITY,
    name              varchar(255) NOT NULL,
    manufacturer_name varchar(255) NOT NULL,
    category          varchar(255) NOT NULL,
    item_number       varchar(30)  NOT NULL,
    description       varchar(1000),
    image_url         varchar(200) NOT NULL,
    created_at        TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (product_id)
);

INSERT INTO products (product_id, name, manufacturer_name, category, item_number, description, image_url)
VALUES (DEFAULT, 'Advil', 'Pfizer', 'pain', 'B085GD8FMF',
        'Whether you have a headache, muscle aches, backaches, menstrual pain, minor arthritis or aches and pains from the common cold, nothing''s stronger on tough pain than Advil.',
        'https://images-na.ssl-images-amazon.com/images/I/71I-R4AidvL._AC_SL1500_.jpg');

-- confirm everything worked
SELECT *
FROM products;