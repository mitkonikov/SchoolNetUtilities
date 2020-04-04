import mysql.connector
import time
import random
import env

DATABASE = mysql.connector.connect(
    host=env.DB_HOST,
    user=env.DB_USER,
    passwd=env.DB_PASS,
    database="db_znam"
)

mycursor = DATABASE.cursor()

def generateData():
    start_time = time.time()

    for r in range(0, 10000):
        sql = "INSERT INTO tbl_scoreboard (Subject, Rank, Score, Player_ID, Q_Correct, Q_Wrong) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (random.randrange(10), random.randrange(5000), random.randrange(500), random.randrange(5000), random.randrange(500), random.randrange(500))

        mycursor.execute(sql, val)

    DATABASE.commit()

    elapsed_time = time.time() - start_time
    print("Took {:.4f} s to generate the data in the database".format(elapsed_time))

def generateRanks():
    start_time = time.time()

    for r in range(1, 50):
        sql = "UPDATE tbl_scoreboard SET Rank = %s, Score = %s WHERE ID = %s"
        val = (random.randrange(5000), random.randrange(5000), r)

        mycursor.execute(sql, val)

    DATABASE.commit()

    elapsed_time = time.time() - start_time
    print("Took {:.4f} s to generate new ranks in the database".format(elapsed_time))

generateRanks()