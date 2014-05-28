#!/usr/bin/python
'''
just for passing pylint check
'''
def sum_num(num1, num2):
    '''
    sum two number, and return the sum
    >>> sum_num(1, 2)
    3
    >>> sum_num(10, -10)
    0
    '''
    return num1 + num2

if __name__ == '__main__':
    import doctest, docTestSample
    doctest.testmod(docTestSample)
