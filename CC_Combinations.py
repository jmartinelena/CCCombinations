import numpy as np
from itertools import product

#Luhn Algorithm
def luhn(ccnumber):
    """Returns true if a given 16-digit integer ccnumber is a valid credit card number, otherwise returns false."""
    cc = [int(x) for x in str(ccnumber)]
    payload = cc[-1]
    digits = cc[:-1:]

    if len(cc) == 16:
        #reversed digits
        rev_digits = digits[::-1] 
        
        for i in range(len(rev_digits)): 
            if i==0 or i%2==0:
                rev_digits[i]*=2
        
        #multiplied digits
        mult_digits = [str(x) for x in rev_digits[::-1]] 

        checksum = 0
        for element in mult_digits:
            esum = 0
            for digit in element:
                esum += int(digit)
            checksum += esum

        if (10-checksum%10) == payload:
            return True
        else:
            return False   
    else:
        raise ValueError("The credit card number must be 16 digits long.")

# Do 10000 random 16 digit combinations, test how many of those are valid cc combinations
# and get the probabilty of a random 16 digit number being a valid cc, then use that
# to estimate how many of the 10^12 combinations are valid cc numbers


# Get the first n combinations of valid cc numbers 
# If I simply use product it will take a lot of time, so I HAVE to use numpy to make it as efficient as possible
# Read this
# https://stackoverflow.com/questions/36435754/generating-a-numpy-array-with-all-combinations-of-numbers-that-sum-to-less-than
# https://stackoverflow.com/questions/1208118/using-numpy-to-build-an-array-of-all-combinations-of-two-arrays/