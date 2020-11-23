import json
import random

count = 0

def clean(DATABASE_PATH, EXPORT_PATH):
    '''
    Puts all the words in one line txt file
    '''

    global count

    database_file = open(DATABASE_PATH, "r", encoding="UTF-8")
    json_file = json.loads(database_file.read())

    resultTXT = ""

    json_list = list(json_file)

    a = range(len(json_list))
    b = random.sample(a, len(a))

    for k in b:
        resultTXT = resultTXT + json_list[k] + " "
        count += 1

    database_file.close()

    export_file = open(EXPORT_PATH, "w+", encoding="UTF-8")
    export_file.write(resultTXT)
    export_file.close()

def printStats():
    print ("===========================================")
    print ("Count of total different words: " + str(count))