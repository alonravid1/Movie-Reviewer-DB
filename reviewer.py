#Load .env file
from dotenv import load_dotenv
import os
import mysql.connector


def connect():
    load_dotenv()
    cnx = mysql.connector.connect(
    user = 'root',
    password =  os.getenv('MYSQL_ROOT_PASSWORD'),
    host = '127.0.0.1',
    database = 'sakila'
    )
    return cnx



def check_reviewer(cursor):
    """
    check if the reviewer table exists
    """
    cursor.execute("""
    show tables;
    """)
    result = cursor.fetchall()
    return (('reviewer', ) in result)

def check_rating(cursor):
    """"
    check if the rating table exists
    """
    cursor.execute("""
    show tables;
    """)
    result = cursor.fetchall()
    return (('rating', ) in result)


def create_reviewer_table(cursor):
    """
    create the reviewer table
    """
    cursor.execute("""
    CREATE TABLE reviewer (
        reviewer_id INT NOT NULL,
        first_name VARCHAR(45) NOT NULL,
        last_name VARCHAR(45) NOT NULL,
        PRIMARY KEY(reviewer_id)
    )
    """)

def create_rating_table(cursor):
    """
    create the review table
    """
    cursor.execute("""
    CREATE TABLE rating(
        film_id SMALLINT NOT NULL,
        reviewer_id INT NOT NULL,
        rating DECIMAL(2,1) NOT NULL,
        FOREIGN KEY(film_id) REFERENCES film(film_id),
        FOREIGN KEY(reviewer_id) REFERENCES reviewer(reviewer_id),
        CHECK (rating >=0 AND rating < 10)
    )
    """)

def create_reviewer(cursor, id):
    """
    creates a new reviewer using the
    input id, and asking for first and
    last names.
    """
    first_name, last_name = input("Enter first and last name").split()
    cursor.execute("""
        INSERT INTO reviewer
        VALUES {}, '{}', '{}'
        """.format(id, first_name, last_name))

def add_review(cursor, film_id):
    pass

def get_film_id(cursor):
    """
    """
    film = input("Please enter a film name")

    cursor.execute("""
        SELECT title, film_id, release_year
        FROM film
        WHERE title = '{}'
        """.format(film))
    result = cursor.fetchall()

    while(len(result) == 0):
        film = input("No such film exists, please enter a new film name: ")
        cursor.execute("""
            SELECT title, film_id, release_year
            FROM film
            WHERE title = '{}'
             """.format(film))
        result = cursor.fetchall()
        
    if(len(result) == 1):
        return result[0][0]
    else:
        print("Please select a film based on it's id from the following list:")
        print(result)
        film = input()
        for movie in result:
            if(movie[0] == film):
               return film
       
def check_id(cursor,id):
    """
    check if the given ID exists in the
    reivewer table
    """
    cursor.execute("""
    SELECT CONCAT(first_name, '', last_name)
    FROM reviewer
    WHERE reviewer_id = {};
    """.format(id))
    result = cursor.fetchone()
    if(len(result) == 0):
        #step 2
        create_reviewer(cursor)
        return None
        #check whether or not to continue to step 3 from 2 or not!
    else:
        #step 3
        print("Hello {}.".format(result))
        return get_film(cursor)


def main():
    cnx = connect()
    cursor = cnx.cursor()
    if(not check_reviewer(cursor)):
        create_reviewer_table(cursor)
    if(not check_rating(cursor)):
        create_rating_table(cursor)

    #step one
    id = input("Please enter your reviewer ID:")
    check_id(cursor, id)
    #remember to check behaviour when the rating is 2.333

    film_id = get_film_id(cursor)
    if(not film_id):
        cursor.execute("""
        INSERT INTO rating
        VALUES 
        """)


    


def main_t():
    cnx = connect()
    cursor = cnx.cursor()
    add_film = "INSERT INTO film (film_id, title, release_year, language_id ) VALUES (%s, %s, %s, %s)"
    val2 = (2000, 'ACADEMY DINOSAUR', 2030, 1)
    cursor.execute(add_film, val2)
    cnx.commit()
    cursor.execute("select * from film where title = 'ACADEMY DINOSAUR'")
    test2 = cursor.fetchall()
    print(test2)
    #get_film(cursor)

if __name__ == '__main__':
    main_t()