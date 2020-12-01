import unittest
import sys
import os
import time

DEBUG_TEST_ARTICLE = False
DEBUG_TIME = True

sys.path.append("C:/GitHub/SchoolNetUtilities")

import wikipedia.xml_to_txt as xml_to_txt

class TestSetCreation(unittest.TestCase):
    def test_parse_article(self):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_path = os.path.join(file_dir, "example_article_wt.txt")
        file = open(file_path, "r", encoding="UTF-8")
        text = file.read()
        file.close()

        if (DEBUG_TEST_ARTICLE):
            print("=======================================================")
            print(text)
            print("=======================================================")

        # parse the file using the wikitextparser
        start_time = time.time()
        parsed = xml_to_txt.parseArticle(text)

        if (DEBUG_TEST_ARTICLE):
            print(parsed)
            print("=======================================================")

        if (DEBUG_TIME):
            elapsed_time = time.time() - start_time
            print("Time elapsed: ", elapsed_time)
            print("=======================================================")

        # parse the file with our modified plain_text function
        start_time = time.time()
        parsedFast = xml_to_txt.parseArticleFast(text)

        if (DEBUG_TEST_ARTICLE):
            print(parsedFast)
            print("=======================================================")

        if (DEBUG_TIME):
            elapsed_time = time.time() - start_time
            print("Time elapsed: ", elapsed_time)
            print("=======================================================")

        # self.assertEqual(parsedFast, parsed)

if __name__ == '__main__':
    unittest.main()