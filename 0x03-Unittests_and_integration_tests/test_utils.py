#!/usr/bin/env python3
'''
A test file to carry out unit test on the utils module
'''
import unittest
from utils import access_nested_map
from parameterized import parameterized


class TestNestedMap(unittest.TestCase):
    ''' A test class for the util module'''

    """ The @parameterized.expand decorator is what allows us to run the same test method multiple times with different data.

    It takes one argument: a list of tuples. Each tuple contains the arguments for one run of the test.

    For each of your provided inputs, we need to create a tuple that contains:

    The nested_map (the dictionary).

    The path (the tuple of keys).

    The expected result (the value the function should return). """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_acces_nested_map(self, nested_map, path, result):
        ''' Test that test the nested map and check if it returns the valid output with a valid input'''

        self.assertEqual(access_nested_map(nested_map, path), result)