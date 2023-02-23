""""""

from __future__ import annotations

__author__ = ''
__docformat__ = 'reStructuredText'

class LargestPrimeIterator():
    
    """
    Generates a prime number based on the upper bound.
    """

    def __init__(self, upper_bound, factor):
        """
        Best and worst case complexity: O(1)
        """
        self.upper_bound = upper_bound
        self.factor = factor
    

    def GCD(self, upper_bound):
        """
        GCD(self,upper_bound) is a function that when called by the __next__ method, will return the largest prime number 
        that is strictly less than the current value of the upper_bound. After the value is computed, the value of upper_bound 
        will be updated by "upper_bound = p * factor".

        Best and worst case complexity: O(N + N*N), N is the upper_bound
        """
        upper_bound = self.upper_bound

        current_upper_bound = upper_bound 
        primes_list = []

        if current_upper_bound < 2: #If 1 or 0, no primes
            primes_list = []

        for i in range(current_upper_bound):
            primes_list.append(i)


        for i in range(2, int(current_upper_bound**0.5)+1): #Only need to check up to sqrt(n)
            if primes_list[i]: #If true, its a prime 
                for j in range(i**2, current_upper_bound, i):
                    primes_list[j] = 0
        return max(primes_list)
    

    def __iter__(self):
        """
        __iter__ makes this class iterable.

        Best and worst case complexity: O(1)
        """
        return self
        

    def __next__(self):
        """
        __next__ calls the next item after the current item.

        Best and worst case complexity: O(1)
        """
        prime_num = self.GCD(self.upper_bound)
        self.upper_bound = self.factor * prime_num
        return prime_num

if __name__ == '__main__':
    x = LargestPrimeIterator(6, 2)
    xi = iter(x)
    print(next(xi))
    print(next(xi))
    print(next(xi))
    print(next(xi))
    print(next(xi))
