#!/usr/bin/env python3
'''
A test file to carry out unit test on the utils module
'''
from unittest import TestCase, mock
from utils import access_nested_map, get_json
from parameterized import parameterized
import requests


class TestAccessNestedMap(TestCase):
    ''' A test class for the util module'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, result):
        ''' Test that test the nested map and check if it returns the valid output with a valid input'''

        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({},('a', ), KeyError),
        ({'a':1}, ('a','b'), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, error):
        ''' A Test that check if exception is raised for wrong input '''
        
        with self.assertRaises(error):
            access_nested_map(nested_map, path)
                    

class TestGetJson(TestCase):
    'A test class to test get_json'

    @parameterized.expand([
        ('http://example.com', {"payload": True}),
        ('http://example.io', {"payload": False}),
    ])
    def test_get_json(self, uri, result):
        ''' Used mock.patch to send mock http request to the request.get'''
        with mock.patch(requests.get) as mock_data:
            mock_data.return_value = result
            response = get_json(uri)
            mock_data.assert_called_once_with(uri)
            self.assertEqual(response, result)