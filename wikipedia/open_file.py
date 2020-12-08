import os
from os import listdir
from os.path import isfile, join
import json

def printFile(file_path, character_max = "max"):
    # Get the absolute path to the file
    if not os.path.isabs(file_path):
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, file_path)

    if not os.path.exists(file_path):
        return

    # Open the file
    file = open(file_path, "r", encoding="UTF-8")
    file_read = ""

    if (character_max == "max"):
        file_read = file.read()
        print(file_read)
        print("Length of the file in chars: ", str(len(file_read)))
        print("Length of the file in words: ", str(len(file_read.split(" "))))
    else:
        # Read it in chunks
        count = 0
        while count < character_max:
            file_chunk = file.read(1024)
            count += 1024
            file_read += file_chunk
        print(file_read)
    
    file.close()

def openJSON(file_path):
    database_file = open(file_path, "r", encoding="UTF-8")
    return json.loads(database_file.read())

def write(file_path, text):
    file = open(file_path, "w+", encoding="UTF-8")
    file.write(text)
    file.close()

def writeJSON(file_name, json_data):
    export_file = open(file_name, "w+", encoding="UTF-8")
    export_file.write(json.dumps(json_data, ensure_ascii = False, indent = 4))
    export_file.close()

def listFiles(dir_path):
    return [f for f in listdir(dir_path) if isfile(join(dir_path, f))]