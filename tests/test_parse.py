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

    def test_parse_decodes_false_into_string(self):
        obj = 'a=false'
        result = parse(obj)
        expected = {'a': 'false'}
        self.assertEqual(result, expected)

    def test_parse_decodes_string_into_string(self):
        obj = 'a=b'
        result = parse(obj)
        expected = {'a': 'b'}
        self.assertEqual(result, expected)

    def test_parse_decodes_whitespaces(self):
        obj = 'a=b%20c'
        result = parse(obj)
        expected = {'a': 'b c'}
        self.assertEqual(result, expected)

    def test_parse_decodes_special_chars(self):
        obj = 'a=%E4%BF%8A'
        result = parse(obj)
        expected = {'a': '俊'}
        self.assertEqual(result, expected)

    def test_parse_decode_ampersand_concats_multiple_items(self):
        obj = 'a=b&c=d'
        result = parse(obj)
        expected = {'a': 'b', 'c': 'd'}
        self.assertEqual(result, expected)

    def test_parse_decode_entries_into_multiple_nested_object(self):
        obj = 'a[b]=c&d[e]=f&d[g]=h'
        result = parse(obj)
        expected = {'a': {'b': 'c'}, 'd': {'e': 'f', 'g': 'h'}}
        self.assertEqual(result, expected)

    def test_parse_decode_list_into_multiple_nested_object(self):
        obj = 'a[0]=1&a[1]=2&a[2]=3&b[0]=q&b[1]=w&b[2]=e'
        result = parse(obj)
        expected = {'a': {'0': '1', '1': '2', '2': '3'}, 'b': {'0':'q', '1':'w', '2':'e'}}
        self.assertEqual(result, expected)