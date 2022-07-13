from multiprocessing.sharedctypes import Value
import numpy as np
from itertools import product, islice
import random

#Luhn Algorithm
def luhn(ccnumber):
    """Returns true if a given 16-digit string ccnumber is a valid credit card number, otherwise returns false."""
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
# https://docs.python.org/3/library/itertools.html#itertools-recipes

def random_products(n):
    "Returns a random selection of n arrays composed of 12 digit combinations from 0 to 9."
    digits = np.array(range(0,10))
    combo = np.tile(digits, (12,1)) # digits but repeated 12 times
    sample = np.empty([n,12], dtype=np.int64)

    i=0
    while i < n:
        # choose a random number from each array in combo and form and array with those chosen numbers
        elem = np.array([comp[random.randint(0, len(comp)-1)] for comp in combo])
        sample[i] = elem
        i+=1
    
    sample = sample.astype(str).tolist()
    numbers = ["".join(row) for row in sample]
    return numbers
    #return np.fromiter(map(int, numbers), dtype=np.int64) # aca hay un error que me esta arruinando la vida :)
    # Numbers that start with 0 get fucked over, meaning that 012345678911 gets turned into 12345678911, so I MUST work with strings

def estimate_probabilty(lastfour):
    "Returns the estimated probability of picking a random number that ends with a given 4 digit sequence (as a string) and it being a valid credit card number."
    sample = random_products(10000)
    sample_append_lastfour = [row+str(lastfour) for row in sample]
    #print(sample_append_lastfour)
    filtered_sample = np.fromiter((luhn(x) for x in sample_append_lastfour), dtype=np.int8)
    result = round(filtered_sample.sum()/filtered_sample.size,1) # Without rounding, this should be a number arround 0.1, so I'm just rounding it to force it to be 0.1
    return (result, result * 10**12)


# Get the first n combinations of valid cc numbers 
# If I simply use product it will take a lot of time, so I HAVE to use numpy to make it as efficient as possible
# Read this
# https://stackoverflow.com/questions/36435754/generating-a-numpy-array-with-all-combinations-of-numbers-that-sum-to-less-than
# https://stackoverflow.com/questions/1208118/using-numpy-to-build-an-array-of-all-combinations-of-two-arrays/
# Nevermind, I have to use strings so I'm not gonna bother with efficiency

# I don't want to create a a large amount of combinations and then filter it, so I have to find an elegant way
# of only generating data that is a possible combination. Sadly, I don't know how to achieve this (yet). (generators? recursion?)
def get_combinations(lastfour, n, mode):
    """input: 
        lastfour: last four digits of a possible credit card as a string
        n: amount of possible combinations you want
        mode: 1 for random or 0 for first n combinations
    output: writes a combinations.txt file with the possible combinations obtained."""
    if mode == 0: #first n
        first12 = islice(product("0123456789", repeat=12), n*15)
        alldigits = ["".join(x)+str(lastfour) for x in first12]
    elif mode == 1: #random n
        first12 = random_products(n*15)
        alldigits = [row+str(lastfour) for row in first12]
    else:
        raise ValueError("Wrong mode. Expected 0 or 1.")

    filtered_sample = np.fromiter((luhn(x) for x in alldigits), dtype=np.bool8)
    keep = np.extract(filtered_sample, alldigits)
    keep = keep[:n]

    with open("combinations.txt", "w", encoding='utf-8') as file:
        for result in keep:
            file.write(result+"\n")


if __name__ == "__main__":
    #print(estimate_probabilty("1510")) #this gives 0, and I hope this is mathematically correct and not another bug
    lastfour = input("Type the last 4 numbers of the credit card: ")
    estimate = estimate_probabilty(lastfour)
    print(f"Theres approximately {estimate[1]} of valid credit cards ending with {lastfour}.")
    n = int(input("How many combinations do you want? Mind you, it takes a long time to calculate them if you choose a big number. n: "))
    mode = int(input(f"Do you want the first {n} combinations of valid credit cards or a {n} random of them? Type \"0\" for the first {n} combinations, otherwise type \"1\" for random ones. mode: "))
    get_combinations(lastfour, n, mode)
    print("Results written to combinations.txt file.")