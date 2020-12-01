import os
import re
from typing import List

import wikipedia.open_file as open_file

txt_files = []
txt_dir_path = None

def init(txt_path):
    global txt_files
    global txt_dir_path
    txt_dir_path = txt_path
    txt_files = open_file.listFiles(txt_path)

def findExampleInText(text, word):
    found = re.search("[.?!\n]([\w, ]+)[ ](" + word + ")([.?!]|([ ][\w\d, ]+[.?!\n]))", text)
    if found != None:
        span = found.span()
        sentence = text[(span[0] + 1):span[1]].lstrip()
        return sentence
    else:
        return None

def findExamples(word):
    lsExamples: List[str]
    lsExamples = []

    count = 0
    for txt in txt_files:
        file = open(os.path.join(txt_dir_path, txt), "r", encoding="UTF-8")
        file_text = file.read()
        example = findExampleInText(file_text, word)

        if (example != None):
            lsExamples.append(example)
            count += 1

            if count == 10:
                break

    return lsExamples