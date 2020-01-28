# mysql_creation.py

import mysql.connector

db = mysql.connector(connect (host = "db-booklib.c5jfpls229sf.us-west-1.rds.amazonaws.com",
                              user="admin", password="", database="BOOKSHELF"))

cur = db.cursor()

#creates latest instance of database as still in early prototyping stages
cur.execute('''DROP DATABASE IF EXISTS BOOKSHELF;
               CREATE DATABASE IF NOT EXISTS BOOKSHELF;
               USE BOOKSHELF;''')

# creates user_id table
cur.execute('''CREATE TABLE IF NOT EXISTS tb_USERS (
    user_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name varchar (255),
    user_email varchar(255),
    user_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );''')

# creates table of book_images
cur.execute ('''CREATE TABLE IF NOT EXISTS tb_BOOK_IMAGES(
    book_images_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    book_info JSON
    );''')

# creates table of a bookshelf with userid, imageids and shelfids
cur.execute('''CREATE TABLE IF NOT EXISTS tb_SHELF (
    shelf_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_ID integer NOT NULL,
    book_images_ID integer,
    book_images_name varchar(255),
    CONSTRAINT user_ID FOREIGN KEY(user_ID)
    REFERENCES tb_USERS(user_ID),
    CONSTRAINT book_images_ID FOREIGN KEY (book_images_ID)
    REFERENCES tb_BOOK_IMAGES(book_images_ID));)''')

db.commit()
