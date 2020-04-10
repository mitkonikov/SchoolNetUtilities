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

def sortRanks():
    start_time = time.time()

    sql = "SELECT ID, Rank, Score FROM tbl_leaderboard"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    myresult = sorted(myresult, key=lambda r: r[2], reverse=True) #ORDER BY Score DESC

    processed = list()

    cRank = 1
    cScore = myresult[0][2]
    lres = len(myresult)
    for i in range(0, lres):
        cList = list(myresult[i])
        score = cList[2]
        oldRank = cList[1]

        if (cScore == score):
            cList[1] = cRank
        else:
            cRank += 1
            cList[1] = cRank
            cScore = score
        
        if (oldRank != cRank):
            processed.append(cList)

    for i in range(0, len(processed)):
        sql = "UPDATE tbl_leaderboard SET Rank = %s WHERE ID = %s"
        val = (processed[i][1], processed[i][0])

        mycursor.execute(sql, val)

    DATABASE.commit()

    elapsed_time = time.time() - start_time
    print("Took {:.4f} s to sort the ranks in the database".format(elapsed_time))

sortRanks()