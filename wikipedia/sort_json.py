import json

count = 0

def loadFile(DATABASE_PATH):
    database_file = open(DATABASE_PATH, "r", encoding="UTF-8")
    result = json.loads(database_file.read())
    database_file.close()
    return result

def sortFile(DATABASE_PATH, EXPORT_PATH):
    json_file = loadFile(DATABASE_PATH)
    sortJSON(json_file, EXPORT_PATH)

def sortJSON(JSON, EXPORT_PATH):
    global count

    PAIRS = []

    for stat in JSON:
        PAIRS.append((JSON[stat], stat))

    PAIRS = sorted(PAIRS, key=lambda pair: pair[0], reverse = True)

    export_file = open(EXPORT_PATH, "w+", encoding="UTF-8")
    export_file.write("{\n")

    line_count = 1
    pairs_len = len(PAIRS)
    for pair in PAIRS:
        if not line_count == pairs_len:
            export_file.write("\t\"" + pair[1] + "\" : " + str(pair[0]) + ",\n")
        else:
            export_file.write("\t\"" + pair[1] + "\" : " + str(pair[0]) + "\n")

        line_count += 1
    
    export_file.write("}")
    export_file.close()

    count = len(PAIRS)

def printStats():
    print ("===========================================")
    print ("Count of total different words: " + str(count))