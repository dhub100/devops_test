import math

def power(a, b):
    return a ** b

def logarithm(a, base):
    if a <= 0:
        raise ValueError('Logarithm of x <= is not defined')
    return math.log(a, base)
