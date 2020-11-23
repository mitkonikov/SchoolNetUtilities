from os import listdir
from os.path import isfile, join
import re
import json
from wikipedia.xml_to_txt import UNWANTED_KEYWORDS

import wikipedia.alphabet as alphabet
import wikipedia.open_file as open_file

DATABASE = {}
countOpen = 0
countWords = []
countSen = [] # Count of Sentences

UNWANTED_CHARS = ['.', ',', ':', '!', '?', ';']
STOP_CHARS = ['.', '!', '?']
IGNORED_WORDS = ["пр", ""]

for l in "абвгдѓжзѕјклљмнњопрстќуфхцчџш":
    IGNORED_WORDS.append(str(l))

def replaceInFile(text):
    import_text = text.replace("\n", " ") # negate the new lines
    import_array = import_text.split(" ") # split the file into an array of words
    return import_array

def cleanFile(text, startSen):
    results = {
        "countWordsCurrent": 0,
        "countSenCurrent": 0,
        "startSen": startSen
    }

    import_array = replaceInFile(text)

    for word in import_array:
        word = word.lower()
        ignore = False
        for u in IGNORED_WORDS:
            if word == u:
                ignore = True
                break

        if ignore:
            continue

        if results["startSen"]:
            for c in STOP_CHARS:
                if not word.find(c) == -1:
                    results["startSen"] = False
                    results["countSenCurrent"] = results["countSenCurrent"] + 1
        elif re.search("[" + alphabet.getAlphabet() + "]", word):
            results["startSen"] = True

        for c in UNWANTED_CHARS: word = word.replace(c, "")

        if word in DATABASE:
            DATABASE[word] = DATABASE[word] + 1
        else:
            DATABASE[word] = 1

        results["countWordsCurrent"] = results["countWordsCurrent"] + 1

    return results

def convert(TXT_PATH):
    global DATABASE
    global countOpen
    global countWords
    global countSen

    countWordsCurrent = 0
    countSenCurrent = 0

    onlyfiles = [f for f in listdir(TXT_PATH) if isfile(join(TXT_PATH, f))]

    startSen = False

    for f in onlyfiles:
        # open a new file
        import_file = open(join(TXT_PATH, f), "r", encoding="UTF-8")
        import_text = import_file.read()
        
        dict = cleanFile(import_text, startSen)
        countWordsCurrent = dict["countWordsCurrent"]
        countSenCurrent = dict["countSenCurrent"]
        startSen = bool(dict["startSen"])

        import_file.close()

        if startSen:
            countSenCurrent = countSenCurrent + 1
            startSen = False

        # Append statistics for each file
        countWords.append(countWordsCurrent)
        countSen.append(countSenCurrent)

        # Reset statistics
        countWordsCurrent = 0
        countSenCurrent = 0
        countOpen = countOpen + 1

        if (countOpen % 1000 == 0):
            print("Opened the {}th file.".format(countOpen))

def printStats():
    print ("===========================================")
    print ("Count of opened .txt files: " + str(countOpen))
    print ("Count of total words: " + str(sum(countWords)))
    print ("Count of total sentences: " + str(sum(countSen)))
    print ("Average word count per article: " + str(sum(countWords) / countOpen))
    print ("Average sentence count per article: " + str(sum(countSen) / countOpen))

def exportFile(DATABASE_PATH):
    open_file.write(DATABASE_PATH, json.dumps(DATABASE, ensure_ascii = False, indent = 4))
    print("DATABASE written!")