import requests
import json
import wikipedia.indexing.config as config
import wikipedia.open_file
import wikipedia.find_examples as find_examples
from typing import List, Dict

url = config.INDEX_API_URL
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def chunkize(data, chunk_size, skip) -> List[Dict]:
    '''
        This function takes in the JSON data and converts it in chunks,
        so it can be easily sent to the server
    '''
    ls = []
    wordsArray = { }
    chunkCount = 0
    skippedCount = 0
    for d in data:
        if (skippedCount < skip):
            skippedCount += 1
            continue

        wordsArray[d] = data[d]
        chunkCount += 1
        if (chunkCount == chunk_size):
            ls.append(wordsArray.copy())
            wordsArray = { }
            chunkCount = 0

    ls.append(wordsArray.copy())
    return ls

def indexWords(DATABASE_FILE, amount, skip):
    '''
        Sends the words dataset to the server's INDEX API
    '''
    db_data = wikipedia.open_file.openJSON(DATABASE_FILE)
    chunks = chunkize(db_data, amount, skip)
    print("Sending ", len(chunks), " chunks to the server.")

    printReqs = 0
    for chunk in chunks:
        chunkBody = {
            "auth": config.INDEX_API_KEY,
            "words": chunk
        }

        req = requests.post(url, data = json.dumps(chunkBody), verify = True, headers = headers)
        if (printReqs < 3):
            print(req.text)
            printReqs += 1

def indexExamples(txt_path, database_path, frq_more_than, frq_less_than, limit_examples_per_word = 10, limit_words = None) -> Dict[str, List]:
    """Generates and sends chunks of examples for each word
        that has frequency below some threshold

    Args:
        txt_path (string): Path of the txt files
        database_path (string): Path of the JSON database file
        frq_threshold (number): Find examples for words only below this threshold
    """

    find_examples.init(txt_path)
    db_data = wikipedia.open_file.openJSON(database_path)
    countWords = 0
    ls_words = []
    for word in db_data:
        if (db_data[word] > frq_more_than and db_data[word] < frq_less_than):
            ls_words.append(word)
            countWords += 1

        if limit_words is not None and countWords >= limit_words:
            break

    print("Count of words:", countWords)
    return find_examples.findWords(ls_words, limit_examples_per_word)

def indexExamples_old(txt_path, database_path, frq_more_than, frq_less_than, limit_examples = None) -> Dict[str, List]:
    """Generates and sends chunks of examples for each word
        that has frequency below some threshold

    Args:
        txt_path (string): Path of the txt files
        database_path (string): Path of the JSON database file
        frq_threshold (number): Find examples for words only below this threshold
    """

    dictExamples = { }
    find_examples.init(txt_path)
    db_data = wikipedia.open_file.openJSON(database_path)
    countWords = 0
    countExamples = 0
    for word in db_data:
        if (db_data[word] > frq_more_than and db_data[word] < frq_less_than):
            exs = find_examples.findExamples(word, 3)
            countExamples += 1
            countWords += 1
            dictExamples[word] = exs.copy()

            if limit_examples is not None and countExamples > limit_examples:
                break

    print("Count of words:", countWords)

    return dictExamples