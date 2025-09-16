#!/usr/bin/env python3
'''
A test file to carry out unit test on the utils module
'''
from unittest import TestCase
from utils import access_nested_map
from parameterized import parameterized


class TestAccessNestedMap(TestCase):
    ''' A test class for the util module'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_acces_nested_map(self, nested_map, path, result):
        ''' Test that test the nested map and check if it returns the valid output with a valid input'''

        self.assertEqual(access_nested_map(nested_map, path), result)