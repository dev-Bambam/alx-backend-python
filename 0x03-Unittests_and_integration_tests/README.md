# Testing Introduction

This project contains unit and integration tests for Python utilities and I learnt about the parameterized decorator which is used to run test on method with multiple input

The @parameterized.expand decorator is what allows us to run the same test method multiple times with different data.

    It takes one argument: a list of tuples. Each tuple contains the arguments for one run of the test.

    For each of your provided inputs, we need to create a tuple that contains:

    The nested_map (the dictionary).

    The path (the tuple of keys).

    The expected result (the value the function should return). 