import unittest
import sys

sys.path.append("C:/GitHub/SchoolNetUtilities")

import wikipedia.txt_to_json as txt_to_json
import wikipedia.find_examples as find_examples

class TestSetCreation(unittest.TestCase):
    def test_convertFile(self):
        txt_to_json.convertFile("Нешто <br />убаво ")
        db = txt_to_json.getDatabaseAndReset()
        self.assertEqual(db, {
            "нешто": 1,
            "убаво": 1
        }, "Failed to match the output database!")

        self.assertEqual(txt_to_json.DATABASE, {}, "Database not empty after reseting!")

    def test_wrong_input_on_parse(self):
        txt_to_json.convertFile("Нешто {убаво ")
        db = txt_to_json.getDatabaseAndReset()
        self.assertEqual(db, {
            "нешто": 1,
            "убаво": 1
        })

    def test_new_line(self):
        txt_to_json.convertFile("Нешто\n убаво ")
        db = txt_to_json.getDatabaseAndReset()
        self.assertEqual(db, {
            "нешто": 1,
            "убаво": 1
        })

    def test_find_example(self):
        e = find_examples.findExampleInText("Положбата е од огромно значење. Територијата, на Република Македонија е вклучена во првиот часовен појас, после запирка.", "часовен")
        self.assertEqual(e, "Територијата, на Република Македонија е вклучена во првиот часовен појас, после запирка.")

if __name__ == '__main__':
    unittest.main()