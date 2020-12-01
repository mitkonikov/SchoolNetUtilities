import json
import wikipedia.open_file as open_file

countSplit = [0, 0]

def splitFile(DATABASE_PATH, EXPORT_PATH_FIRST, EXPORT_PATH_SECOND, MIN_NUM):
    global countSplit

    database_file = open(DATABASE_PATH, "r", encoding="UTF-8")
    json_file = json.loads(database_file.read())

    output_big = {}
    output_small = {}

    for stat in json_file:
        if json_file[stat] >= MIN_NUM:
            output_big[stat] = json_file[stat]
            countSplit[0] = countSplit[0] + 1
        else:
            output_small[stat] = json_file[stat]
            countSplit[1] = countSplit[1] + 1

    database_file.close()

    open_file.writeJSON(EXPORT_PATH_FIRST, output_big)
    open_file.writeJSON(EXPORT_PATH_SECOND, output_small)

    print("Done Spliting!")

def printStats():
    print ("===========================================")
    print ("Count of words with more occurrences than MIN_NUM: " + str(countSplit[0]))
    print ("Count of words with less occurrences than MIN_NUM: " + str(countSplit[1]))
    print ("Proportion (more/less*100%): " + str(countSplit[0] / countSplit[1] * 100) + "%")