from os import listdir
from os.path import isfile, join
import re

import wikipedia.alphabet as alphabet
import wikipedia.open_file as open_file

from typing import List

DATABASE = {}
countOpen = 0
countWords = []
countSen = [] # Count of Sentences

UNWANTED_CHARS = ['.', ',', ':', '!', '?', ';']
STOP_CHARS = ['.', '!', '?', '{', '}']
IGNORED_WORDS = ["пр", "стр", "км", "м", ""]

# pay attention: this is not the whole alphabet (e and i are counted as words)
for l in "абвгдѓжзѕјклљмнњопрстќуфхцчџш":
    IGNORED_WORDS.append(str(l))

def replaceInFile(text):
    import_text = text.replace("\n", " ") # negate the new lines
    import_array = import_text.split(" ") # split the file into an array of words
    return import_array

def convertFile(text):
    global DATABASE
    global countSen
    global countWords
    global countOpen

    fileSen = 0

    allWords: List[str]
    allWords = re.findall("[" + alphabet.getAlphabet() + "]+[ \n\.\,\;\:\!\?]", text)
    
    startSen = False
    for word in allWords:
        if re.match("[" + alphabet.getAlphabet() + "]+[ \n]", word):
            startSen = True

        for ending in STOP_CHARS:
            if word.endswith(ending):
                if startSen:
                    startSen = False
                    fileSen += 1
                
        cleanWord = word[:len(word) - 1].lower()

        if cleanWord in DATABASE:
            DATABASE[cleanWord] = DATABASE[cleanWord] + 1
        else:
            DATABASE[cleanWord] = 1

    # Append statistics for each file
    countWords.append(len(allWords))
    countSen.append(fileSen)

    countOpen = countOpen + 1
    if (countOpen % 1000 == 0):
        print("Opened the {}th file.".format(countOpen))

def convert(TXT_PATH):
    onlyfiles = open_file.listFiles(TXT_PATH)

    for f in onlyfiles:
        # open a new file
        import_file = open(join(TXT_PATH, f), "r", encoding="UTF-8")
        import_text = import_file.read()
        
        convertFile(import_text)

        import_file.close()

    print("Clearing up unwanted words...")
    for word in IGNORED_WORDS:
        if word in DATABASE:
            del DATABASE[word]

    print("Done converting.")

def printStats():
    print ("===========================================")
    if (countOpen > 0):
        print ("Count of opened .txt files: " + str(countOpen))
    
    print ("Count of total words: " + str(sum(countWords)))
    print ("Count of total sentences: " + str(sum(countSen)))
    
    if (countOpen > 0):
        print ("Average word count per article: " + str(sum(countWords) / countOpen))
        print ("Average sentence count per article: " + str(sum(countSen) / countOpen))

def getDatabaseAndReset():
    global DATABASE
    db = DATABASE
    DATABASE = {}
    countSen = 0
    countOpen = 0
    countWords = 0
    return db

def exportFile(DATABASE_PATH):
    open_file.writeJSON(DATABASE_PATH, DATABASE)
    print("DATABASE written!")