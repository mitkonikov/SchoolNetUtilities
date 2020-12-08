from os import listdir
from os.path import isfile, join

## NOTE: This is now deprecated
# The following code was a usage example:
#   - Go through every TXT file ranking them by their word count
"""
    indexing.compile(TXT_PATH)
    indexing.sortByWordsPerArticle(TXT_PATH, BYWORDS_SORT)
    splitter.splitFile(BYWORDS_SORT, BYWORDS_FRQ_MORE, BYWORDS_FRQ_LESS, 1000)
"""

def compile(TXT_PATH):
    print(listFiles(TXT_PATH)[:50])
    print("Finished listing all the files.")

def listFiles(TXT_PATH):
    return [f for f in listdir(TXT_PATH) if isfile(join(TXT_PATH, f))]

def sortByWordsPerArticle(TXT_PATH, RESULT_FILE, CHECK_ID=False):
    import wikipedia.mysql_connection as mysql_connection

    # list all the txt files of articles
    FILES = listFiles(TXT_PATH)

    json_dict = {}

    file_count = 0
    max_word_count = 0
    max_prev_word_count = -1
    for FILE_PATH in FILES:
        # open a new file
        import_file = open(join(TXT_PATH, FILE_PATH), "r", encoding="UTF-8")
        # split the file into an array of words
        import_array = import_file.read().split(" ")

        # count the words
        words_count = 0
        for word in import_array:
            if not (word == "." or word == " "):
                words_count += 1

        # update the max word count
        max_word_count = max(max_word_count, words_count)

        ID = -1
        if CHECK_ID:
            # get the ID from mySQL according the file name
            ID_array = mysql_connection.getID(FILE_PATH.replace(".txt", ""))
            if len(ID_array) == 1:
                ID = ID_array[0][0]

        # remember the file name and the word count in the json_dict
        if CHECK_ID:
            json_dict[ID] = words_count
        else:
            json_dict[str(file_count + 1)] = words_count

        # print if ID doesn't match the file count
        if CHECK_ID:
            if not ID == file_count:
                print("Suspecious: ID {} is not equal to file_count {}".format(ID, file_count))

        # up the file count and on every 100th file print the status
        file_count += 1
        if (file_count % 100 == 0):
            print ("Counted the {}th file.".format(file_count))

            # if the max_word_count has changed, print it
            if not max_prev_word_count == max_word_count: 
                print ("  => maximum word count in a single file: " + str(max_word_count))
                max_prev_word_count = max_word_count

        # close the file for good measures :D
        import_file.close()

    print("Finished counting all the files")

    # sort the json_dict before writing it
    import wikipedia.sort_json as sort_json
    sort_json.sortJSON(json_dict, RESULT_FILE)

    print("Finished sorting and writing the json")