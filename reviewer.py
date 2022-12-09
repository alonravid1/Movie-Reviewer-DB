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



def check_reviewer_table(cursor):
    """
    check if the reviewer table exists
    """
    cursor.execute("""
    show tables;
    """)
    result = cursor.fetchall()
    return (('reviewer', ) in result)

def check_rating_table(cursor):
    """"
    check if the rating table exists
    """
    cursor.execute("""
    show tables;
    """)
    result = cursor.fetchall()
    return (('rating', ) in result)

def check_rating(rating):
    """
    check that the given rating is a valid input
    return True if it is, False if not
    """
    try:
        decimals = 0
        splt_rating = str(rating).split(".")
        if(len(splt_rating) == 2):
            #check if the number has decimal digits
            decimals = len(splt_rating[1])
            
        if(float(rating) < 0):
            return False
        if(float(rating) >= 10):
            return False
        if(decimals > 1):
            return False
        return True
    except(Exception):
        return False


    

def check_reviewer_id(reviewer_id):
    """
    check that the given id is a valid input
    return True if it is, False if not
    """
    try:
        if(int(reviewer_id) < 1):
            return False
        return True
    except(Exception):
        return False

    

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
    cnx.commit()

def create_rating_table(cnx, cursor):
    """
    create the review table
    """
    cursor.execute("""
        CREATE TABLE rating (
            film_id SMALLINT UNSIGNED NOT NULL,
            reviewer_id INT NOT NULL,
            rating DECIMAL(2,1) NOT NULL,
            PRIMARY KEY(film_id, reviewer_id),
            FOREIGN KEY(film_id)
                REFERENCES film(film_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY(reviewer_id)
                REFERENCES reviewer(reviewer_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            CHECK (rating >= 0 AND rating < 10)
        );
        """)
    cnx.commit()
    
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

def add_review(cnx, cursor, film_id, reviewer_id):
    """
    recieves a film id, reviewer id and asks for a rating until
    it recieves a valid one. It then adds the new rating to the
    rating table, or updates an existing one if it exsists already.
    """
    rating = input("Please enter a rating from 0 to 9.9: ")
 
    while (not check_rating(rating)):
        rating = input("""Invalid rating, please enter a rating between 0 and 9.9,
        with only one decimal digit: """)

    insert_review = """
        INSERT INTO rating
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY
            UPDATE rating = %s
        """
    cursor.execute(insert_review, [film_id, reviewer_id, rating, rating])
    cnx.commit()

def get_film_id(cursor):
    """
    recieves a film name, returns it's ID if it exsits
    and has only one release, otherwise prints all
    releases and their IDs and asks the user to pick a specific id.
    """
    film = input("Please enter a film name: ")

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
            return result[0][1]

        else:
            print("Please select a film based on its ID from the following list:")
            for movie in result:
                print("movie: {} | id: {} | release year: {}".format(movie[0], movie[1], movie[2]))
            film_id = input()
            for movie in result:
                try:
                    if(int(movie[1]) == int(film_id)):
                        return film_id
                except ValueError:
                    pass
            result = [] #sets result's length to 0


        

def auth_reviewer(cnx, cursor, id):
    """
    check if the given ID exists in the
    reivewer table, create a new reviewer with
    the givne id if not
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
    if(not check_reviewer_table(cursor)):
        create_reviewer_table(cnx, cursor)
    if(not check_rating_table(cursor)):
        create_rating_table(cnx, cursor)

    #step one
    reviewer_id = input("Please enter your reviewer ID: ")
    while(not check_reviewer_id(reviewer_id)):
        reviewer_id = input("Please enter a valid reviewer ID: ")
   


    #step two inside
    name = auth_reviewer(cnx, cursor, reviewer_id)


    #step 3
    print("Hello {}.".format(name))
    film_id = get_film_id(cursor)

    #step 4
    if(film_id != None):
       add_review(cnx, cursor, film_id, reviewer_id)

    #step 5
    i = 0
    get_rating = """
        SELECT f.title, CONCAT(rev.first_name, ' ', rev.last_name), rate.rating
        FROM film f, reviewer rev, rating rate
        WHERE rate.film_id = f.film_id
            AND rev.reviewer_id = rate.reviewer_id
        """
    cursor.execute(get_rating)

    #print up to 100 ratings
    for rating in cursor:
        print("movie: {} | reviewer: {} | rating: {}".format(rating[0], rating[1], rating[2]))
        i += 1
        if(i == 99):
            break


    #remember to check behaviour when the rating is 2.333


def main_t():
    cnx = connect()
    cursor = cnx.cursor()
    
    i = 0
    get_rating = """
        SELECT f.title, CONCAT(rev.first_name, ' ', rev.last_name), rate.rating
        FROM film f, reviewer rev, rating rate
        WHERE rate.film_id = f.film_id
            AND rev.reviewer_id = rate.reviewer_id
        """
    cursor.execute(get_rating)
    #for (q_title, q_name, q_rating) in cursor:
        #print("".format(q_title, q_name, q_rating))
    for rating in cursor:
        print("movie: {} | reviewer: {} | rating: {}".format(rating[0], rating[1], rating[2]))
        i += 1
        if(i == 99):
            break


if __name__ == '__main__':
    main()