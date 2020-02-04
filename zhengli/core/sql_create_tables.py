import mysql.connector
import config from config

host_= db-booklib.c5jfpls229sf.us-west-1.rds.amazonaws.com

def connect():
    """ Connect to the mySQL database server """
    conn = None
    try:
        # read connection parameters
        db = mysql.connector(connect(host=host_,
                     user="admin",
                     passwd="",
                     db="BOOKSHELF")

        # create a cursor
        cur = db.cursor()
        
        # Config settings
        SET @@time_zone = 'SYSTEM';
        SET FOREIGN_KEY_CHECKS=1;

        # execute a statement

        #creates latest instance of database as still in early prototyping stages

        cur.execute('''CREATE DATABASE IF NOT EXISTS BOOKSHELF;
                   USE BOOKSHELF;''')

        cur.execute('''CREATE TABLE IF NOT EXISTS tb_USERS (
                    user_ID integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    user_name varchar (255) UNIQUE,
                    user_email varchar(255) UNIQUE,
                    user_password varchar(255),
                    user_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    user_last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
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

        # commit the db commands
        db.commit()

    except (Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
connect()
