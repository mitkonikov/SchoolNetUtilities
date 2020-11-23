import time
import mysql.connector

import wikipedia.indexing as indexing
import wikipedia.sort_json as sort_json
import wikipedia.config as config

DATABASE = mysql.connector.connect(
    host = config.MYSQL_HOST,
    user = config.MYSQL_USER,
    passwd = config.MYSQL_PASSWORD,
    database = config.MYSQL_DATABASE
)

mycursor = DATABASE.cursor()

NAME_SEL = "./" + config.OUT_NAME
TXT_PATH = NAME_SEL + "-exports/"

def readFiles():
	start_time = time.time()

	FILES = indexing.listFiles(TXT_PATH)

	elapsed_time = time.time() - start_time
	print("Took {:.4f} s to list all the files".format(elapsed_time))

	return FILES

def indexRows():
	start_time = time.time()

	rowInserted = 0

	FILES = readFiles()

	for count in range(0, len(FILES)):
		sql = "INSERT INTO tbl_index (ID, Filename, Bot) VALUES (%s, %s, %s)"
		val = (count + 1, FILES[count].replace('.txt', ''), False)

		mycursor.execute(sql, val)

		rowInserted += 1

		if (rowInserted % 50 == 0):
			print("Inserted the " + str(count) + "th row.")

		DATABASE.commit()
		
	elapsed_time = time.time() - start_time
	print("Took {:.4f} s to index the files in the database".format(elapsed_time))

def getID(FILE_NAME):
	sql = "SELECT ID FROM tbl_index WHERE Filename = %s"
	val = (FILE_NAME, )

	mycursor.execute(sql, val)
	myresult = mycursor.fetchall()

	RESULT = []
	for r in myresult:
		RESULT.append(r)

	return RESULT

def addWords(DATABASE_PATH):
	start_time = time.time()

	json_dict = sort_json.loadFile(DATABASE_PATH)
	
	WORD_COUNT = 0
	for word in json_dict:
		if (not word == "") and (not word == " "):
			sql = "INSERT INTO tbl_words (ID, Word, Type, Occurrences, Mistake, Wiki_Frq) VALUES (%s, %s, %s, %s, %s, %s)"
			val = (WORD_COUNT + 1, word, 0, "", 0, json_dict[word])

			mycursor.execute(sql, val)

			if (WORD_COUNT % 500 == 0):
				print("Inserted the " + str(WORD_COUNT) + "th word.")

			DATABASE.commit()
			WORD_COUNT += 1

	elapsed_time = time.time() - start_time
	print("Took {:.4f} min to add the words in the database".format(elapsed_time/60))