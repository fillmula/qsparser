from unittest import TestCase
from qsparser import parse


class TestParse(TestCase):

    def test_parse_decodes_int_into_string(self):
        qs = 'a=5'
        result = parse(qs)
        expected = {'a': '5'}
        self.assertEqual(result, expected)

    def test_parse_decodes_float_into_string(self):
        qs = 'a=5.5'
        result = parse(qs)
        expected = {'a': '5.5'}
        self.assertEqual(result, expected)

    def test_parse_decodes_true_into_string(self):
        qs = 'a=true'
        result = parse(qs)
        expected = {'a': 'true'}
        self.assertEqual(result, expected)
