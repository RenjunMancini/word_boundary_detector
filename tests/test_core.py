import unittest

from word_boundary_detector import split_words


class TestSplitWords(unittest.TestCase):
    def test_simple_sentence(self):
        self.assertEqual(split_words("Hello world"), ["Hello", "world"])

    def test_apostrophe_keeps_word_together(self):
        self.assertEqual(split_words("don't stop"), ["don't", "stop"])

    def test_curly_apostrophe(self):
        self.assertEqual(split_words("it\u2019s fine"), ["it\u2019s", "fine"])

    def test_hyphen_keeps_word_together(self):
        self.assertEqual(split_words("well-known fact"), ["well-known", "fact"])

    def test_leading_apostrophe_is_dropped(self):
        # A joiner with no preceding word character does not start a token.
        self.assertEqual(split_words("'tis the season"), ["tis", "the", "season"])

    def test_trailing_hyphen_is_dropped(self):
        self.assertEqual(split_words("end-"), ["end"])

    def test_combining_mark_stays_with_base(self):
        # 'e' + combining acute accent is one grapheme.
        text = "caf\u0065\u0301"
        self.assertEqual(split_words(text), ["caf\u0065\u0301"])

    def test_numbers_are_words(self):
        self.assertEqual(split_words("version 2.0"), ["version", "2", "0"])

    def test_punctuation_is_separator(self):
        self.assertEqual(split_words("hello, world!"), ["hello", "world"])

    def test_empty_string(self):
        self.assertEqual(split_words(""), [])

    def test_whitespace_only(self):
        self.assertEqual(split_words("   \t\n"), [])

    def test_mixed_joiners(self):
        self.assertEqual(split_words("mother-in-law's house"),
                         ["mother-in-law's", "house"])


if __name__ == "__main__":
    unittest.main()
