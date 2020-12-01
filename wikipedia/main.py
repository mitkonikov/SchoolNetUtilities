# https://dumps.wikimedia.org/mkwiki/20201101/

import os
import time
import sys

sys.path.append("C:/GitHub/SchoolNetUtilities")

import wikipedia.xml_to_txt as xml_to_txt
import wikipedia.txt_to_json as txt_to_json
import wikipedia.suffix_cleaner as suffix_cleaner
import wikipedia.sort_json as sort_json
import wikipedia.splitter as splitter
import wikipedia.json_words_txt as json_words_txt
# import wikipedia.indexing as indexing
import wikipedia.open_file as open_file
import wikipedia.find_examples as find_examples

NAME = "wikipedia-mk"
NAME_SEL = os.path.join(os.path.dirname(__file__), "./" + NAME)

FRQ_FROM_ALL = "./wikipedia-mk-frq-from-all/"

XML_FILE = os.path.join(os.path.dirname(__file__), "./RAW/articles.xml")
TXT_PATH = NAME_SEL + "/exports/"
DATABASE_FILE = NAME_SEL + "/database.txt"
SORTED_FILE = NAME_SEL + "/database-sorted.txt"
SCLEAN_FILE = NAME_SEL + "/database-sclean.txt"
FRQ_MORE_FILE = NAME_SEL + "/database-frq-more.txt"
FRQ_LESS_FILE = NAME_SEL + "/database-frq-less.txt"
BYWORDS_SORT = NAME_SEL + "/bywords-sorted.txt"
BYWORDS_FRQ_MORE = NAME_SEL + "/bywords-frq-more.txt"
BYWORDS_FRQ_LESS = NAME_SEL + "/bywords-frq-less.txt"

ALL_FRQ_MORE = NAME_SEL + "/database-frq-more.txt"
WORDS_TXT_FILE = NAME_SEL + "/database-words.txt"

def main():
    print ("Processing...")
    start_time = time.time()

    ### NOTE: WARNING:
    ### OPENING THE XML FILE WITH ANY EDITOR CAN CAUSE THE EDITOR TO FREEZE
    ### THESE FILES ARE HUGE! EVEN OPENING THE DIRECTORY OF ALL OF THE TXT
    ### FILES, CAN CAUSE THE OS TO FREEZE!
    ###
    ### INSTEAD, USE THE WIKIMEDIA FILES AS SMALL EXAMPLES IF YOU WANT TO SEE
    ### THE STRUCTURE OF THE ARTICLES (OR JUST READ A KNOWN ARTICLE USING THE FOLLOWING
    ### FUNCTION IN THE XML_TO_TXT CONVERTER)

    # In order to get an example article from the XML file
    '''
    text = xml_to_txt.readArticle(XML_FILE, "Географија на Македонија")
    open_file.write("./example_article.txt", text)
    text_filtered = xml_to_txt.parseArticleFast(text)
    open_file.write("./example_filtered_fast.txt", text_filtered)
    txt_to_json.convertFile(text_filtered)
    txt_to_json.printStats()
    text_db = txt_to_json.DATABASE
    open_file.writeJSON("./example_db_fast.txt", text_db)
    '''

    ### NOTE: These scripts are all single-threaded, so it takes some time to process the whole Wikipedia
    ### If someone would be kind enough to make them multi-threaded, that would be nice

    # Convert the big .XML file into small .TXT files for every article
    # while doing some initial filtering (for more info, check the xml_to_txt converter)
    '''
    #input("Press any key to start the XML to TXT conversion...")
    xml_to_txt.convert(XML_FILE, TXT_PATH)
    xml_to_txt.printStats()
    
    open_file.printFile(os.path.join(TXT_PATH, "Географија на Македонија.txt"), character_max = 1000)
    '''

    # Dealing with BOT-generated files
    # This is user command line simulation
    # The commands are: ls, min, filter, stepdelete, delete
    '''
    REPEATING_FILES = None
    FILTER_LIST = []
    FROM_NUMBER = 1
    STARTS_WITH_STRING = ""
    STEP_DELETE = False
    MIN = 500

    while True:
        INPUT = input("> ").split()
        if INPUT[0] == "ls":
            print("Listing files with most frequent start-strings...")
            REPEATING_FILES = xml_to_txt.listRepeatingFiles(TXT_PATH, MIN=MIN)
            REPEATING_FILES = sorted(REPEATING_FILES, key=lambda pair: pair[1], reverse = True)
            print(REPEATING_FILES)
        elif INPUT[0] == "min":
            MIN = int(INPUT[1])
        elif INPUT[0] == "filter":
            STARTS_WITH_STRING = ""
            for x in INPUT[1:]:
                STARTS_WITH_STRING = STARTS_WITH_STRING + " " + str(x)
            STARTS_WITH_STRING = STARTS_WITH_STRING.lstrip()

            FILTER_LIST = xml_to_txt.listRFstartswith(TXT_PATH, FROM_NUMBER, STARTS_WITH_STRING)
            print(FILTER_LIST[:20], "...")
            print("Length of list: " + str(len(FILTER_LIST)))
        elif INPUT[0] == "stepdelete":
            STEP_DELETE = not STEP_DELETE
            print ("Step delete is set to {}".format(STEP_DELETE))
        elif INPUT[0] == "delete":
            for FILE in FILTER_LIST:
                NEXT_FILE = os.path.join(TXT_PATH, FILE)

                if STEP_DELETE:
                    STEP = input("Next file: {}".format(NEXT_FILE))
                    if not STEP == "go":
                        break

                if os.path.exists(NEXT_FILE):
                    os.remove(NEXT_FILE)
                else:
                    print("The file does not exist")
        elif INPUT[0] == "continue":
            break
        else:
            print('Unknown command. Maybe you want to "continue"?')
    '''

    # txt_to_json goes to every txt file in the directory and counts the words in a dictionary
    '''
    input("Press any key to start the TXT to JSON conversion...")
    txt_to_json.convert(TXT_PATH)
    txt_to_json.exportFile(DATABASE_FILE)
    txt_to_json.printStats()
    '''
    

    # (OPTIONAL) Cleaning the JSON database file from words that are the same
    # with some suffix. Ex: книгаТА => книга
    # NOTE: This is not yet developed right, here's a contra-example:
    # година => годи
    '''
    suffix_cleaner.clean(DATABASE_FILE, SCLEAN_FILE)
    suffix_cleaner.printStats()
    '''

    # Sorts the json file and splits it according to word occurences
    '''
    input("Press any key to sort and split the JSON file...")
    sort_json.sortFile(DATABASE_FILE, SORTED_FILE)
    sort_json.printStats()
    splitter.splitFile(SORTED_FILE, FRQ_MORE_FILE, FRQ_LESS_FILE, 10)
    splitter.printStats()
    '''

    # Puts all of the words in one line .txt file
    '''
    json_words_txt.clean(ALL_FRQ_MORE, WORDS_TXT_FILE)
    json_words_txt.printStats()
    '''

    # Finds an example sentence that contains this word
    
    find_examples.init(TXT_PATH)
    examples = find_examples.findExamples("Географија")
    print('\n'.join(examples))
    
    # Go through every TXT file ranking them by their word count
    '''
    indexing.compile(TXT_PATH)
    indexing.sortByWordsPerArticle(TXT_PATH, BYWORDS_SORT)
    splitter.splitFile(BYWORDS_SORT, BYWORDS_FRQ_MORE, BYWORDS_FRQ_LESS, 1000)
    '''
    
    # Index the files in the MySQL Database
    '''import wikipedia.mysql_connection as mysql_connection'''

    '''
    input("Press any key to start indexing the files in the database...")
    mysql_connection.indexRows()
    '''
    
    # Add every word from the frq_more_file in the database
    '''mysql_connection.addWords(FRQ_MORE_FILE)'''

    # If you want to open a specific file without opening the directory
    # Why? Opening the directory causes the OS to index the files in the directory
    # making you wait, so just use this function
    ### open_file.printFile(os.path.join(TXT_PATH, "Географија на Македонија.txt"), CHARACTER_MAX=500)

    elapsed_time = time.time() - start_time
    print("Time elapsed: ", elapsed_time)

if __name__ == '__main__':
    main()