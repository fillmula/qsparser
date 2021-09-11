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
        qs = 'a=false'
        result = parse(qs)
        expected = {'a': 'false'}
        self.assertEqual(result, expected)

    def test_parse_decodes_string_into_string(self):
        qs = 'a=b'
        result = parse(qs)
        expected = {'a': 'b'}
        self.assertEqual(result, expected)

    def test_parse_decodes_whitespaces(self):
        qs = 'a=b%20c'
        result = parse(qs)
        expected = {'a': 'b c'}
        self.assertEqual(result, expected)

    def test_parse_decodes_special_chars(self):
        qs = 'a=%E4%BF%8A'
        result = parse(qs)
        expected = {'a': '俊'}
        self.assertEqual(result, expected)

    def test_parse_decodes_multiple_items_to_a_single_object(self):
        qs = 'a=b&c=d'
        result = parse(qs)
        expected = {'a': 'b', 'c': 'd'}
        self.assertEqual(result, expected)

    def test_parse_decodes_entries_into_multiple_nested_objects(self):
        qs = 'a[b]=c&d[e]=f&d[g]=h'
        result = parse(qs)
        expected = {'a': {'b': 'c'}, 'd': {'e': 'f', 'g': 'h'}}
        self.assertEqual(result, expected)

    def test_parse_decodes_list_into_multiple_nested_object(self):
        qs = 'a[0]=1&a[1]=2&a[2]=3&b[0]=q&b[1]=w&b[2]=e'
        result = parse(qs)
        expected = {'a': ['1', '2', '3'], 'b': ['q' ,'w', 'e']}
        self.assertEqual(result, expected)

    def test_parse_decodes_dicts_in_lists(self):
        qs = 'a[0][n]=John&a[0][a]=15&a[1][n]=Peter&a[1][a]=18&b[0][n]=Jack&b[0][a]=17'
        result = parse(qs)
        expected = {'a': [{'n': 'John', 'a': '15'},
                          {'n': 'Peter', 'a': '18'}],
                    'b': [{'n': 'Jack', 'a': '17'}]}
        self.assertEqual(result, expected)

    def test_parse_decodes_lists_in_dicts(self):
        qs = 'a[0][n][0]=John&a[0][n][1]=15&a[1][n][0]=Peter&a[1][n][1]=18&b[0][n][0]=Jack&b[0][n][1]=17'
        result = parse(qs)
        expected = {'a': [{'n': ['John', '15']},
                          {'n': ['Peter', '18']}],
                    'b': [{'n': ['Jack', '17']}]}
        self.assertEqual(result, expected)
