class myContextManager:
    def __enter__(self):
        print('Entering the block')

        return None # The __enter__() must always return something as the return value is what will be attached to the 'as' clause variable when using the custom manager

    def multiply(self, num):
        return num * num
    
    def __exit__(self, exec_type, exec_value, traceback):
        print('Existing the block')

with myContextManager() as mult:
    number = 2
    pow = mult.multiply(number)
    print(f'{number} raised to power {number} equals {pow}')

print('I am outside the context now')