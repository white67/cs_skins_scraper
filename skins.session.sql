create database skins_valued CHARACTER SET utf8mb4 collate utf8mb4_0900_ai_ci;

-- @block use
use skins_valued;

-- @block create
create table buffids (
    item_name varchar(100) primary key,
    buff_id int not null
);

-- @block create
create table skin_offers (
    offer_id int not null auto_increment primary key,
    sale_id int not null,
    item_full_name varchar(100),
    item_name varchar(100),
    stattrak boolean,
    sale_price int,
    sale_cur varchar(20),
    sale_price_pln decimal(10, 2),
    sale_status varchar(100),
    wear decimal(18,16),
    exterior varchar(50),
    rarity varchar(50),
    item_collection varchar(100),
    item_category varchar(100),
    souvenir boolean,
    stickers int,
    pattern int,
    finish int,
    inspect_link varchar(255),
    custom_name varchar(255),
    weapon_name varchar(70),
    url_slug varchar(255),
    trade_banned boolean,
    trade_ban_end datetime,
    scrape_time datetime,
    marketplace varchar(50)
);

-- @block alter
alter table skin_offers add column goods_id int;

-- @block create
create table buff_prices (
    goods_id int not null primary key,
    item_full_name varchar(100),
    lowest_offer_cny decimal(10,2),
    lowest_offer_pln decimal(10,2),
    offers_count int,
    highest_order_cny decimal(10,2),
    highest_order_pln decimal(10,2),
    orders_count int,
    img varchar(255),
    last_update datetime
);