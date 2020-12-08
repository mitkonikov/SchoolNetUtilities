import os
import re
from typing import List, Dict

import wikipedia.open_file as open_file

txt_files = []
txt_dir_path = None

def init(txt_path):
    global txt_files
    global txt_dir_path
    txt_dir_path = txt_path
    txt_files = open_file.listFiles(txt_path)

def findExampleInText(text: str, word: str, sentence_size: int):
    found = re.findall("[.?!\n](([\w ]+)[ ](" + word + ")([.?!]|([ ][\w\d, ]+[.?!\n])))", text)
    result = []
    if len(found) > 0:
        for sen in range(0, len(found)):
            if (len(found[sen][0]) < sentence_size):
                result.append(found[sen][0].lstrip().rstrip('\n').rstrip())
    return result

def findExamples(word, amount = 10, sentence_size = 100) -> List[str]:
    lsExamples: List[str]
    lsExamples = []

    count = 0
    for txt in txt_files:
        file = open(os.path.join(txt_dir_path, txt), "r", encoding="UTF-8")
        file_text = file.read()
        examples = findExampleInText(file_text, word, sentence_size)

        if (len(examples) > 0):
            lsExamples.extend(examples)
            count += len(examples)

            if count > amount:
                break

    return lsExamples

def findWords(list_words: List[str], amount_per_each = 10, sentence_size = 100) -> Dict[str, List[str]]:
    """For each word in the list, finds some amount of example sentences containing that word.

    Args:
        list_words (List[str]): List of words to search for
        amount_per_each (int, optional): The number of sentences to return. Defaults to 10.
        sentence_size (int, optional): Maximum sentence size. Defaults to 100.

    Returns:
        Dict[str, List[str]]: Dictionary where each word is mapped to a list of sentences
    """
    dictExamples: Dict[str, List[str]]
    dictCount: Dict[str, int]
    dictExamples = { }
    dictCount = { }

    # Create the dictionary of the words
    for word in list_words:
        dictExamples[word] = []
        dictCount[word] = 0

    for txt in txt_files:
        if len(list_words) == 0:
            break

        file = open(os.path.join(txt_dir_path, txt), "r", encoding="UTF-8")
        file_text = file.read()

        # In each file, check for each word
        for word in list_words:
            if dictCount[word] >= amount_per_each:
                list_words.remove(word)
                continue

            examples = findExampleInText(file_text, word, sentence_size)
            if (len(examples) > 0):
                dictExamples[word].extend(examples)
                dictCount[word] += len(examples)

    return dictExamples