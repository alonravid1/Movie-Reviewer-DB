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


def create_reviewer_table(cnx, cursor):
    """
    create the reviewer table
    """

    cursor.execute("""
    CREATE TABLE reviewer (
        reviewer_id INT NOT NULL PRIMARY KEY,
        first_name VARCHAR(45) NOT NULL,
        last_name VARCHAR(45) NOT NULL
    );
    """)
    #cnx.commit()


def create_rating_table(cnx, cursor):
    """
    create the review table
    """
    cursor.execute("""
        CREATE TABLE rating (
            film_id SMALLINT NOT NULL,
            reviewer_id INT NOT NULL,
            rating DECIMAL(2,1) NOT NULL,
            FOREIGN KEY(film_id)
                REFERENCES film (film_id),
            FOREIGN KEY (reviewer_id)
                REFERENCES reviewer (reviewer_id),
            CHECK (rating >= 0 AND rating < 10)
        );
        """)
    #cnx.commit()
    print("blah")
    
def create_reviewer(cnx, cursor, id):
    """
    creates a new reviewer using the
    input id, and asking for first and
    last names.
    """
    first_name, last_name = input("Enter first and last name: ").split(' ')

    insert_reviewer ="""
        INSERT INTO reviewer
        VALUES (%s, %s, %s);
        """
    cursor.execute(insert_reviewer, [id, first_name, last_name])
    cnx.commit()

def add_review(cursor, film_id):
    pass

def get_film_id(cursor):
    """
    """
    film = input("Please enter a film name")

    cursor.execute("""
        SELECT title, film_id, release_year
        FROM film
        WHERE title = %s;
        """,[film])
    result = cursor.fetchall()

    while(True):
        #runs until it the user enters a valid input
        if(len(result) == 0):
            film = input("No such film exists, please enter a new film name: ")
            cursor.execute("""
                SELECT title, film_id, release_year
                FROM film
                WHERE title = %s;
                """,[film])
            result = cursor.fetchall()

        elif(len(result) == 1):
            return result[0][0]

        else:
            print("Please select a film based on its ID from the following list:")
            print(result)
            film_id = input()
            for movie in result:
                if(movie[0] == film_id):
                    return film_id
            result = [] #sets result's length to 0
        

def check_id(cnx, cursor, id):
    """
    check if the given ID exists in the
    reivewer table
    """

    get_name = """
        SELECT CONCAT(first_name, ' ', last_name)
        FROM reviewer
        WHERE reviewer_id = %s;
        """

    cursor.execute(get_name, [id])
    result = cursor.fetchone()
    if(result == None):
        #step 2
        create_reviewer(cnx, cursor, id)
        cursor.execute(get_name,[id])
        result = cursor.fetchone()
    #the result is formmated as ('name', )
    return result[0]

def main():
    cnx = connect()
    cursor = cnx.cursor()
    if(not check_reviewer(cursor)):
        create_reviewer_table(cnx, cursor)
    if(not check_rating(cursor)):
        create_rating_table(cnx, cursor)

    #step one
    id = input("Please enter your reviewer ID: ")

    #step two inside
    name = check_id(cnx, cursor, id)


    #step 3
    print("Hello {}.".format(name))
    film_id = get_film_id(cursor)
    if(film_id != None):
        # cursor.execute("""
        # INSERT INTO rating
        # VALUES 
        # """)
        print(film_id)

    #remember to check behaviour when the rating is 2.333

    


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
    main()