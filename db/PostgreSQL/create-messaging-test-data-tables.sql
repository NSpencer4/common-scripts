CREATE DATABASE messaging_app;

CREATE TABLE users
(
    user_id    INT GENERATED ALWAYS AS IDENTITY,
    username   varchar(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id)
);

CREATE TABLE messages
(
    message_id INT GENERATED ALWAYS AS IDENTITY,
    user_id    INT NOT NULL,
    room_id    INT NOT NULL,
    message    varchar(1000),
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (message_id),
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON DELETE SET NULL,
    CONSTRAINT fk_room_id
        FOREIGN KEY (room_id)
            REFERENCES chat_rooms (room_id)
            ON DELETE SET NULL
);

CREATE TABLE chat_rooms
(
    room_id INT GENERATED ALWAYS AS IDENTITY,
    name    varchar(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (room_id)
);