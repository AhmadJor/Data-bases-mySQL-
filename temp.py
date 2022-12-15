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
    host='127.0.0.1',
    database='sakila'
)

cursor = cnx.cursor(buffered=True)

cursor.execute("""
CREATE TABLE if NOT EXISTS reviewer (
  reviewer_id INT UNSIGNED PRIMARY KEY,
  first_name varchar(45) NOT NULL,
  last_name varchar(45) NOT NULL,
  CHECK (REGEXP_LIKE(reviewer_id, '^[0-9]+$')),
  CHECK (REGEXP_LIKE(first_name, '^[a-z|A-Z]+$')),
  CHECK (REGEXP_LIKE(last_name, '^[a-z|A-Z]+$'))
);
""")

cursor.execute("""
CREATE TABLE if NOT EXISTS rating (
  film_id smallint UNSIGNED,
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

insert_reviewer = """INSERT INTO reviewer(reviewer_id,first_name, last_name) VALUES (%s, %s ,%s)"""
reviewer_per_id = """SELECT * FROM reviewer WHERE reviewer_id = %s"""
films_by_film_name = """SELECT * FROM film WHERE title = %s"""
films_by_film_id = """SELECT * FROM film WHERE film_id = %s"""
ratings_by_film_and_reviewer_id = """SELECT * FROM rating WHERE film_id = %s And reviewer_id = %s"""
insert_rating = """INSERT INTO rating (film_id,reviewer_id, rating) VALUES (%s, %s ,%s)"""
update_rating = """UPDATE rating SET rating = %s WHERE film_id = %s AND reviewer_id = %s"""
final_output = """SELECT f.title,concat(re.first_name, ' ' ,re.last_name ) ,r.rating
    FROM rating as r,film as f,reviewer as re 
    WHERE reviewer.ID = reviewer_id and r.film_id = f.film_id
    LIMIT 100
    """
know = 0
while True:
    reviewer_id = input("please insert your id : ")
    while True:
        try:
            reviewer_id = int(reviewer_id)
        except ValueError:
            reviewer_id = input("please insert your id : ")
            continue
        cursor.execute(reviewer_per_id % int(reviewer_id))
        result = cursor.fetchone()
        if (result is not None):
            break
        # step number 2
        first_name = input("insert your first name :")
        last_name = input("insert your last name :")
        value = (int(reviewer_id), first_name, last_name)
        try:
            cursor.execute(insert_reviewer, value)
            cursor.execute(reviewer_per_id % int(reviewer_id))
            result = cursor.fetchone()
            break
        except Error as e:
            reviewer_id = input("please insert your id : ")
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
        cursor.execute(films_by_film_name, [film_name])
        result = cursor.fetchall()
        if not result:
            print("the film doesn't exist")
            flag = 0
            continue
        if len(result) > 1:
            for rows in result:
                print(str(rows[0]) + " " + rows[3])
            fId = input("please insert film id : ")
            try:
                fId = int(fId)
            except ValueError:
                flag = 1
                continue
            cursor.execute(films_by_film_id % int(fId))
            if cursor.fetchone() is not None:
                film_id = int(fId)
                break
            else:
                continue
        else:
            film_id = result[0][0]
            break
    rate = input("please insert a rating : ")
    while True:
        try:
            rate = float(rate)
        except ValueError:
            print("invalid input")
            rate = input("please insert a rating : ")
            continue
        cursor.execute(ratings_by_film_and_reviewer_id, [film_id, reviewer_id])
        result = cursor.fetchone()
        if (result is not None):
            try:
                cursor.execute(update_rating, [float(rate), int(film_id), int(reviewer_id)])
                break
            except Error as e:
                rate = input("please insert a rating : ")
                continue
        else:
            try:
                cursor.execute(insert_rating, [int(film_id), int(reviewer_id), float(rate)])
                break
            except Error as e:
                rate = input("please insert a rating : ")
                continue
    cnx.commit()
    cursor.execute(final_output)
    result = cursor.fetchall()
    for row in result:
        print(row[0] + " " + row[1] + " " + str(row[2]))
