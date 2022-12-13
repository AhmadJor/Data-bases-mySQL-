import os
import mysql.connector
from mysql.connector import Error
# Load dotenv file
from dotenv import load_dotenv

load_dotenv()
# Read the password from the environment variable
password = os.getenv('MYSQL_ROOT_PASSWORD')

cnx = mysql.connector.connect(
    user='root',
    password=password,
    host='localhost',
    database='sakila'
)

cursor = cnx.cursor(buffered=True)

cursor.execute("""
CREATE TABLE if NOT EXISTS reviewer (
  reviewer_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  first_name varchar(45) NOT NULL,
  last_name varchar(45) NOT NULL,
  CHECK (REGEXP_LIKE(reviewer_id, '^[0-9]+$')),
  CHECK (REGEXP_LIKE(first_name, '^[a-z|A-Z]+$')),
  CHECK (REGEXP_LIKE(last_name, '^[a-z|A-Z]+$'))
);

""")

cursor.execute("""
CREATE TABLE if NOT EXISTS rating (
  film_id smallint UNSIGNED AUTO_INCREMENT,
  reviewer_id INT UNSIGNED,
  rating decimal(2,1) NOT NULL,
  PRIMARY KEY (film_id, reviewer_id),
  FOREIGN KEY (film_id)
    REFERENCES film (film_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (reviewer_id)
    REFERENCES reviewer (reviewer_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CHECK(REGEXP_LIKE(rating, '^[0-9]\\.[0-9]$'))
);
""")
cnx.commit()

insert_statement = "INSERT INTO reviewer(reviewer_id,first_name, last_name) VALUES (%s, %s ,%s)"
reviewer_per_id = "SELECT * FROM reviewer WHERE reviewer_id = '%s'"
all_by_film_name = "SELECT * FROM film WHERE title = '%s'"""
all_films_by_film_id = "SELECT * FROM film WHERE film_id = '%s'"
all_ratings_by_film_id = "SELECT * FROM rating WHERE film_id = '%s'"
know = 0
while True:
    reviewer_id = input("please insert your id : ")
    while True:
        try:
            id = int(reviewer_id)
            try:
                cursor.execute(reviewer_per_id % id)
                result = cursor.fetchone()
            except:
                break
        except ValueError:
            reviewer_id = input("please insert your id : ")
            continue
    # step number 2

    first_name = input("insert your first name :")
    last_name = input("insert your last name :")
    while True:
        try:
            #print(reviewer_id + first_name +last_name)
            value = (int(reviewer_id), first_name, last_name)
            print("here")
            cursor.execute(insert_statement, value)
            print("here 1")
            cnx.commit()
            cursor.execute(reviewer_per_id % int(reviewer_id))
            print("here 2")
            result = cursor.fetchone()
            break
        except Error as e:
            first_name = input("insert your first name :")
            last_name = input("insert your last name :")
            continue
    cnx.commit()
    # step number 3
    print(("Hello, " + result[1] + " " + result[2]))
    film_id = -1
    flag = 1
    while True:
        if flag:
            print("insert a film name : ")
        else:
            print("insert a different film name: ")
        film_name = input()

        cursor.execute(all_by_film_name, [film_name])
        result = cursor.fetchall()
        if not result:
            print("the film doesn't exist")
            flag = 0
            continue

        cursor.execute(all_by_film_name, [film_name])
        count = cursor.fetchone()
        if count[0] > 1:
            for rows in result:
                print(str(rows[0]) + " " + rows[3])
            # take care of invalid input here
            fId = input("please insert film id : ")
            cursor.execute(all_films_by_film_id, [fId])
            if cursor.fetchone() is not None:
                film_id = int(fId)
                break
            else:
                continue
        else:
            film_id = result[0]
            break
    rate = input("insert a rating :")
    while True:
        try:
            cursor.execute(all_ratings_by_film_id, [film_id[0]])
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO rating (film_id,reviewer_id, rating) VALUES (%s, %s ,%s)",
                               (int(film_id[0]), int(id), float(rate)))
                break
            else:
                cursor.execute("UPDATE rating SET reviewer_id, rating WHERE film_id = '%s', rating = '%s'"""
                               % (film_id[0], rate))
        except Error as e:
            rate = input("insert a rating :")
    cnx.commit()
    # till here
    cursor.execute("""SELECT f.title,concat(re.first_name, ' ' ,re.last_name ) ,r.rating
    FROM rating as r,film as f,reviewer as re 
    WHERE re.ID = reviewer_id and r.film_id = f.film_id
    """)
    result = cursor.fetchall()
    for row in result:
        print(row[0] + " " + row[1] + " " + str(row[2]))
