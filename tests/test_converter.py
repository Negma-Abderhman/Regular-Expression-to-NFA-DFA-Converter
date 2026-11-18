import itertools
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from regex_converter import (
    RegexError, build_nfa, build_dfa, nfa_accepts, dfa_accepts, convert
)


class ConverterTests(unittest.TestCase):
    def test_suggested_expressions_and_language_equivalence(self):
        expressions = ["0", "01", "0|1", "0*", "1+", "(0|1)*011",
                       "0(0|1)*1", "(0|1)*", "(01)+"]
        words = ["".join(bits) for length in range(6)
                 for bits in itertools.product("01", repeat=length)]
        for regex in expressions:
            with self.subTest(regex=regex):
                nfa, dfa = convert(regex)
                for word in words:
                    self.assertEqual(nfa_accepts(nfa, word), dfa_accepts(dfa, word),
                                     (regex, word))

    def test_invalid_alphabet(self):
        for regex in ["a", "012", "0c1"]:
            with self.subTest(regex=regex):
                with self.assertRaisesRegex(RegexError, "invalid symbol"):
                    build_nfa(regex)

    def test_invalid_syntax(self):
        for regex in ["0|", "|0", "*0", "0(", "()", "0||1", "0)"]:
            with self.subTest(regex=regex):
                with self.assertRaises(RegexError):
                    build_nfa(regex)

    def test_plus_means_one_or_more(self):
        nfa, dfa = convert("1+")
        for word, expected in [("", False), ("1", True), ("11", True),
                               ("111", True), ("0", False), ("10", False)]:
            self.assertEqual(nfa_accepts(nfa, word), expected)
            self.assertEqual(dfa_accepts(dfa, word), expected)

    def test_every_dfa_state_has_two_transitions(self):
        _, dfa = convert("(0|1)*011")
        for state in dfa["states"]:
            self.assertIn((state, "0"), dfa["transitions"])
            self.assertIn((state, "1"), dfa["transitions"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
