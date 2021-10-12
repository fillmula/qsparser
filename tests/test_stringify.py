from unittest import TestCase
from qsparser import stringify


class TestStringify(TestCase):

    def test_stringify_encodes_int_into_int(self):
        obj = {'a': 5}
        result = stringify(obj)
        expected = 'a=5'
        self.assertEqual(result, expected)

    def test_stringify_encodes_float_into_float(self):
        obj = {'a': 5.5}
        result = stringify(obj)
        expected = 'a=5.5'
        self.assertEqual(result, expected)

    def test_stringify_encodes_true_into_true(self):
        obj = {'a': True}
        result = stringify(obj)
        expected = 'a=true'
        self.assertEqual(result, expected)

    def test_stringify_encodes_false_into_false(self):
        obj = {'a': False}
        result = stringify(obj)
        expected = 'a=false'
        self.assertEqual(result, expected)

    def test_stringify_encodes_string_into_string(self):
        obj = {'a': 'b'}
        result = stringify(obj)
        expected = 'a=b'
        self.assertEqual(result, expected)

    def test_stringify_encodes_whitespaces(self):
        obj = {'a': 'b c'}
        result = stringify(obj)
        expected = 'a=b%20c'
        self.assertEqual(result, expected)

    def test_stringify_encodes_special_chars(self):
        obj = {'a': '俊'}
        result = stringify(obj)
        expected = 'a=%E4%BF%8A'
        self.assertEqual(result, expected)

    def test_stringify_concats_multiple_items_with_the_ampersand(self):
        obj = {'a': 'b', 'c': 'd'}
        result = stringify(obj)
        expected = 'a=b&c=d'
        self.assertEqual(result, expected)

    def test_stringify_encodes_dict_into_multiple_entries(self):
        obj = {'a': {'b': 'c'}, 'd': {'e': 'f', 'g': 'h'}}
        result = stringify(obj)
        expected = 'a[b]=c&d[e]=f&d[g]=h'
        self.assertEqual(result, expected)

    def test_stringify_encodes_list_into_multiple_entries(self):
        obj = {'a': [1, 2, 3], 'b': ['q', 'w', 'e']}
        result = stringify(obj)
        expected = 'a[0]=1&a[1]=2&a[2]=3&b[0]=q&b[1]=w&b[2]=e'
        self.assertEqual(result, expected)

    def test_stringify_encodes_nested_items_into_a_long_string(self):
        original = {"_includes": [{"favorites": {"_includes": ["user"]}}]}
        expected = '_includes[0][favorites][_includes][0]=user'
        result = stringify(original)
        self.assertEqual(result, expected)
