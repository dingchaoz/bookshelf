# mysql_creation.py

import mysql.connector
import config from config


#creates latest instance of database as still in early prototyping stages
def create_db(cur):
    cur.execute('''CREATE DATABASE IF NOT EXISTS BOOKSHELF;
                   USE BOOKSHELF;''')

# creates user_id table
def create_user_id_tb(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS tb_USERS (
        user_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_name varchar (255) UNIQUE,
        user_email varchar(255) UNIQUE,
        user_password varchar(255),
        user_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        user_last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );''')

# creates table of book_images
def create_book_image_tb(cur):
    cur.execute ('''CREATE TABLE IF NOT EXISTS tb_BOOK_IMAGES(
        book_images_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
        book_info JSON
        );''')

# creates table of a bookshelf with userid, imageids and shelfids
def create_shelf_tb(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS tb_SHELF (
        shelf_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_ID integer NOT NULL,
        book_images_ID integer,
        book_images_name varchar(255),
        CONSTRAINT user_ID FOREIGN KEY(user_ID)
        REFERENCES tb_USERS(user_ID),
        CONSTRAINT book_images_ID FOREIGN KEY (book_images_ID)
        REFERENCES tb_BOOK_IMAGES(book_images_ID));)''')

def create_bookshelf_db:
    params = config()
    db = mysql.connector(connect (**params)

    cur = db.cursor()
    # Config settings
    SET @@time_zone = 'SYSTEM';
    SET FOREIGN_KEY_CHECKS=1;

    # create database and tables
    create_db(cur)
    create_user_id_tb(cur)
    create_book_image_tb(cur)
    create_shelf_tb(cur)

    # commit the db commands
    db.commit()
