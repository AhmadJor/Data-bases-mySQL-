import os
import mysql.connector 
cnx = mysql.connector.connect( user = 'root' ,password ='A7mad.jorban', host='localhost',database = "sakila")
cursor = cnx.cursor()
#cursor = cnx.cursor(prepared=True)
cursor = cnx.cursor(buffered=True)
cursor.execute("DROP TABLE IF EXISTS `reviewer` ;")
cursor.execute("DROP TABLE IF EXISTS `rating` ;")

def isDigit(x):
    return x >= '0' and x <= '9'
def isValid_rating(rating):
    if len(rating) == 3:
        return isDigit(rating[0]) and rating[1] == '.' and isDigit(rating[2])
    return False

def isNumber(id):
    for digit in id:
        if not isDigit(digit):
            return False
    return True

cursor.execute("""
    CREATE TABLE reviewer (
      ID smallint NOT NULL PRIMARY KEY,
      first_name varchar(45) NOT NULL,
      last_name varchar(45) NOT NULL 
    );
""")

cursor.execute("""
    CREATE TABLE  rating (
      film_id smallint NOT NULL UNIQUE,
      reviewer_id INT NOT NULL UNIQUE,
      rating decimal(2,1) NOT NULL
    );
""")
insert_statement = "INSERT INTO reviewer (ID,first_name, last_name) VALUES (%s, %s ,%s)"

while True:
    while True:
        print("please insert your id : ")
        id = input()
        if isNumber(id):
            break

    cursor.execute("""SELECT * FROM reviewer WHERE ID = '%s'""" % (int(id)))
    result = cursor.fetchone() 
    #step number 2
    if result is None:
        print("insert your first name :")
        first_name = input()
        print("insert your last name :")
        last_name = input()
        value = (int(id) ,first_name ,last_name)
        cursor.execute(insert_statement, value)
    cursor.execute("""SELECT * FROM reviewer WHERE ID = '%s'""" % (int(id)))
    result = cursor.fetchone()
    #step number 3
    print (("Hello, " + result[1] + " " + result[2]))
    film_id = -1
    flag = 1
    while True:
        if flag:
            print("insert a film name : ")
        else:
            print("insert a different film name: ")
        film_name = input()

        cursor.execute("""SELECT * FROM film WHERE title = '%s'""" %film_name)
        result = cursor.fetchall()
        if not result:
            print("the film doesn't exist")
            flag = 0
            continue
        
        cursor.execute("""SELECT Count(*) FROM film WHERE title = '%s'""" %film_name)
        count = cursor.fetchone()
        
        if count[0] > 1:
            for rows in result:
                print (str(rows[0]) +" " + rows[3])
            # take care of invalid input here
            print("please insert film id : ")
            fId = input()
            cursor.execute("""SELECT * FROM film WHERE film_id = '%s'""" %int(fId))
            if cursor.fetchone() is not None:
                film_id=int(fId)
                break
            else:
                continue
        else:
            film_id = result[0]
            break
    while True:
        print("insert a rating :")
        rate = input()
        if isValid_rating(rate):
            break

    cursor.execute("""SELECT * FROM rating WHERE film_id = '%s'""" %int(film_id[0]) )
    if  cursor.fetchone() is not None :
        cursor.execute("DELETE FROM rating WHERE film_id = '%s'""" %int(film_id[0]))
    cursor.execute("INSERT INTO rating (film_id,reviewer_id, rating) VALUES (%s, %s ,%s)",(int(film_id[0]) ,int(id) , float(rate)))


    cursor.execute("""SELECT f.title,concat(re.first_name, ' ' ,re.last_name ) ,r.rating
    FROM rating as r,film as f,reviewer as re 
    WHERE re.ID = reviewer_id and r.film_id = f.film_id
    """ )
    result = cursor.fetchall()
    for row in result:
        print(row[0] + " " + row[1] + " " + str(row[2]))



