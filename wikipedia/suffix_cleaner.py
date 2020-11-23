import json

countDeleted = 0

def clean(DATABASE_PATH, EXPORT_PATH):
    global countDeleted

    fix = ["от", "те", "та", "те", "то", "та", 
            "ов", "ве", "ва", "ве", "во", "ва", 
            "он", "не", "на", "не", "но", "на"]

    database_file = open(DATABASE_PATH, "r", encoding="UTF-8")
    json_file = json.loads(database_file.read())

    for stat in list(json_file):
        for f in fix:
            if stat.endswith(f):
                if not len(stat) == len(f):
                    rootWord = stat[:(len(stat) - len(f))]
                    if rootWord in json_file:
                        uses = json_file[stat]
                        json_file[rootWord] = json_file[rootWord] + uses
                        del json_file[stat]
                        countDeleted = countDeleted + 1
                        break

    database_file.close()

    export_file = open(EXPORT_PATH, "w+", encoding="UTF-8")
    export_file.write(json.dumps(json_file, ensure_ascii = False, indent = 4))
    export_file.close()

def printStats():
    print ("===========================================")
    print ("Count of double entries: " + str(countDeleted))