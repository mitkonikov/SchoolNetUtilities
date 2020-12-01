import unittest
import sys

sys.path.append("C:/GitHub/SchoolNetUtilities")

import wikipedia.filtering

class TestSetCreation(unittest.TestCase):
    def test_clear_curly_brackets(self):
        input = """{{starts with}}
            == Население ==
{{Something|{{Something}}}}{{Else}}

            === Населување и етнографски процеси}} ===
            """

        expected = """
            == Население ==


            === Населување и етнографски процеси ===
            """

        output = wikipedia.filtering.clearCurlyBrackets(input)
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()