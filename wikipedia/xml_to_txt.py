import re
import sys
import os
import time

from xml.etree import ElementTree as ET
from html import unescape

import wikipedia.alphabet as alphabet
import wikipedia.config
import wikipedia.wikitext_plain_text
import wikipedia.filtering
import wikitextparser as wtp

from multiprocessing import Pool

THREADS = 8
PUSH_ONCE = 10
poolQueue = []
for x in range(THREADS): poolQueue.append([])
export_path = ""

DEBUG_PRINT_TITLE = False

countPages = 0
countTitles = 0
countTexts = 0
outsiders = 0

UNWANTED_PAGES = wikipedia.config.UNWANTED_PAGES
UNWANTED_KEYWORDS = wikipedia.config.UNWANTED_KEYWORDS
UNWANTED_STARTS = [".", ",", "!", "?"]
ALPHABET = alphabet.getAlphabet()

notAlphabet = re.compile("[^" + ALPHABET + "\d\w ]")
imageRemover = re.compile("\[\[Податотека:.+\]\][ \n]")
htmlTagRemover = re.compile('(\[[^\s]+ )|(<.*?>)')
headerRemover = re.compile("([\=]+.+[\=]+.+\n)|(<br />)")
galleryRemover = re.compile("<gallery>((\n)|.)*?</gallery>")
externalLinksRemover = re.compile("[\=]+[ ]+(Поврзано|Наводи|Надворешни врски)[ ]+[\=]+")

def convertArticle(title, text):
    global export_path
    export = open(export_path + title + ".txt", "w+", encoding='UTF8')                
    export_text = parseArticle(text)
    export.write(export_text)
    export.close()

def convert(FILE_NAME, EXPORT_PATH):
    global export_path
    export_path = EXPORT_PATH

    start_time = time.time()

    parser = ET.iterparse(FILE_NAME)

    # if export directory doesn't exist, create it
    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)

    inPage = False
    skipToNextPage = False
    
    global countPages
    global countTitles
    global countTexts
    global outsiders

    global UNWANTED_PAGES
    global UNWANTED_KEYWORDS
    global UNWANTED_STARTS

    global ALPHABET

    prev_title_start = ""
    currentTitle = ""

    for event, element in parser:
        # NOTE: When parsing the .xml file, there is not tag parent-child relationships
        # hence we are using the variable 'inPage' 

        # element is a whole element
        elementTag = element.tag
        position = elementTag.find("}")
        elementClean = elementTag.replace(elementTag[:(position + 1)], "")
        if elementClean == 'page':
            countPages = countPages + 1
            if (countPages % 100) == 0:
                print("Processed pages: " + str(countPages))
            inPage = True
            skipToNextPage = False
        
        # if the tag is a title tag
        if (not skipToNextPage) and inPage and elementClean == 'title':
            currentTitle = element.text

            # to avoid freezing you can uncomment this
            # when i wrote this, i forgot that the pages are not sorted
            # so this really SPAMS the console with a lot of text, BE WARNED
            #if not currentTitle[0] == prev_title_start:
            #    print("From now, the titles start with " + currentTitle[0] + " <= PAGE: " + str(countPages))
            #    prev_title_start = currentTitle[0]

            failed = False
            if re.search("^\d", currentTitle):
                failed = True
                skipToNextPage = True
            else:
                for name in UNWANTED_PAGES:
                    if currentTitle.lower().startswith((name + ":")):
                        failed = True
                        skipToNextPage = True
                        break
                for keyword in UNWANTED_KEYWORDS:
                    if re.search(keyword, currentTitle.lower()):
                        failed = True
                        skipToNextPage = True
                        break

            if not failed:
                countTitles = countTitles + 1
                
                if re.search("[^абвгдѓежзѕијклљмнњопрстќуфхцчџш'“„\- ()[\]\d I\/.,\w]", currentTitle.lower()):
                    outsiders = outsiders + 1
                    # print(currentTitle)

        if (not skipToNextPage) and inPage and elementClean == 'text':
            # NOTE: We only classify pages that have more than 200 characters to eliminate the BOT-created pages
            if not element.text == None and len(element.text) > 200:
                countTexts = countTexts + 1
                
                # This removes any unwanted characters from the titles of the pages
                # so we don't get these characters in the text file names
                currentTitle = re.sub(notAlphabet, '', currentTitle)

                export = open(EXPORT_PATH + currentTitle + ".txt", "w+", encoding='UTF8')                
                export_text = parseArticleFast(element.text)
                export.write(export_text)
                export.close()

                if DEBUG_PRINT_TITLE: print("Exported: ", currentTitle)

                #if countTexts < 10:
                    #print ("===============================================================")
                    #print (export_text)
                    #print ("===============================================================")
            inPage = False

        element.clear()
    
    elapsed_time = time.time() - start_time
    print("Time it took to convert the pages: ", elapsed_time)

def readArticle(FILE_NAME, TITLE):
    parser = ET.iterparse(FILE_NAME)

    RESULT_STRING = ""

    inPage = False
    skipToNextPage = False
    
    foundPAGE = False
    for event, element in parser:
        # element is a whole element
        elementTag = element.tag
        position = elementTag.find("}")
        elementClean = elementTag.replace(elementTag[:(position + 1)], "")
        # print(elementClean)

        # if the element is page
        if elementClean == 'page':
            inPage = True
            skipToNextPage = False
        
        # if we are inside a page element
        # and now the element is the title of the page
        if (not skipToNextPage) and inPage and elementClean == 'title':
            currentTitle = element.text
            if currentTitle == TITLE:
                # we are in the page we want to view
                foundPAGE = True

        if foundPAGE and (not skipToNextPage) and inPage and elementClean == 'text':
            RESULT_STRING = element.text

            foundPAGE = False
            break
    
    return RESULT_STRING

def parseArticleFast(text):
    """
        We try to get as close to the wikitextparser but much faster
    """

    # clear the image attachments and links
    text = re.sub(imageRemover, '', text)
    text = re.sub(galleryRemover, '', text)
    text = wikipedia.filtering.clearCurlyBrackets(text)

    # replace everything after "Надворешни врски"
    links_location = re.search(externalLinksRemover, text)
    if links_location != None:
        text = text[:links_location.span()[0]]
        
    # remove headings and break lines
    text = re.sub(headerRemover, '\n', text)

    text = wikipedia.filtering.clearLinks(text)
    text = text.replace('\'', '')

    # remove html tags
    text = re.sub(htmlTagRemover, '', text)

    # remove ref tags
    # text = re.sub('\[[^\s]+ ', '', text)
    text = text.replace(']', '')

    text = unescape(text) # unascape characters
    return text

def parseArticle(text: str) -> str:
    """
        Parses and filters an article. It uses the `wikitextparser` and custom logic.
    """

    # clear the image attachments and links
    text = re.sub("\[\[Податотека:.+\]\][ \n]", '', text)
    text = wikipedia.filtering.clearCurlyBrackets(text)

    # replace everything after "Надворешни врски"
    links_location = re.search("[\=]+[ ]+(Поврзано|Наводи|Надворешни врски)[ ]+[\=]+", text)
    if links_location != None:
        text = text[:links_location.span()[0]]
        
    # remove headings and break lines
    text = re.sub("([\=]+.+[\=]+.+\n)|(<br />)", '\n', text)

    # parse the file using the wikitextparser
    parsed = wtp.parse(text)

    return parsed.plain_text()

def filterArticle(TEXT: str) -> str:
    """
        DEPRECATED
        ----------

        This was our own function for cleaning up an article.
        
        Use the `parseArticle` function to filter an article.
    """

    global UNWANTED_PAGES
    global UNWANTED_KEYWORDS
    global UNWANTED_STARTS
    
    export_text = ""

    # NOTE: Custom Regex for deleting links
    # ex:      [[needs to be deleted|words that stay]]
    #          [[needs to be deleted| <= this is deleted
    #
    # result:                        words that stay]]
    # print(re.findall("\[\[[абвгдѓежзѕијклљмнњопрстќуфхцчџшАБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ\w\d ]+\|", TEXT))
    TEXT = re.sub("\[\[Податотека:.+\]\][ \n]", '', TEXT)
    TEXT = re.sub("\[\[[" + ALPHABET + "\w\d ]+\|", '', TEXT)
    TEXT = re.sub("\(\d+[ ]?(км|стр|м|)[ \.]?\)|\d+[ ]?(км|стр|м)[ |\.]", "", TEXT)
    TEXT = wikipedia.filtering.clearCurlyBrackets(TEXT)

    # replace everything after "Надворешни врски"
    links_location = re.search("[\=]+[ ]+(Поврзано|Наводи|Надворешни врски)[ ]+[\=]+", TEXT)
    if links_location != None:
        TEXT = TEXT[:links_location.span()[0]]

    # remove headings
    TEXT = re.sub("[\=]+.+[\=]+.+\n", '\n', TEXT)

    REPLACEMENTS = [ ['[', ''], 
                     [']', ''],
                     ['—', 'е'],
                     ['-', 'е'],
                     ["'", ''] ]

    for r in REPLACEMENTS:
        TEXT = TEXT.replace(r[0], r[1])

    # For each word
    for word in re.findall("[" + ALPHABET + "\d\.\,\:\!\?]+[ \n]", TEXT):
        failed = False
        for starts in UNWANTED_STARTS:
            if word.startswith(starts):
                failed = True
                break
        
        if not failed:
            export_text = export_text + word

    return export_text

def printStats():
    print ("===========================================")
    print ("Count of Pages: " + str(countPages))
    print ("Count of Titles: " + str(countTitles))
    print ("Count of Texts: " + str(countTexts))
    print ("Count of Outsiders: " + str(outsiders))

def listRepeatingFiles(TXT_PATH: str, MIN=5):
    import wikipedia.indexing as indexing
    FILES = indexing.listFiles(TXT_PATH)

    prev_start = ""
    count_up = 0

    RESULT = []

    FILE_COUNT = 0
    for FILE in FILES:
        NOW = FILE[:3]
        if not NOW == prev_start:
            if count_up > MIN:
                RESULT.append((prev_start, count_up, FILE_COUNT))
            prev_start = NOW
            count_up = 1
        else:
            count_up += 1

        FILE_COUNT += 1
        
    print ("Counted {} files".format(FILE_COUNT))
    print ("Found {} different suspicious entries".format(len(RESULT)))
    return RESULT

def listRFstartswith(TXT_PATH, FROM_NUMBER, STARTS_WITH):
    import wikipedia.indexing as indexing
    FILES = indexing.listFiles(TXT_PATH)

    RESULT = []

    trigger = False
    for i in range(int(FROM_NUMBER), len(FILES)):
        FILE = FILES[i]
        NOW = FILE[:len(STARTS_WITH)]

        if NOW == STARTS_WITH:
            RESULT.append(FILE)
            trigger = True
        else:
            if trigger:
                break

    return RESULT

def shellRun(xml_path, txt_path):
    convert(xml_path, txt_path)
    printStats()
    print("BREAK")

if __name__ == "__main__":
    xml_path = sys.argv[1]
    txt_path = sys.argv[2]
    shellRun(xml_path, txt_path)