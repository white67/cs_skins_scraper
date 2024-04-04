create database skins_valued CHARACTER SET utf8mb4 collate utf8mb4_0900_ai_ci;

-- @block use
use skins_valued;

-- @block create
create table buffids (
    item_name varchar(100) primary key,
    buff_id int not null
);