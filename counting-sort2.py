#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'countingSort' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def countingSort(arr):
    if not arr:
        return []

    # Legnagyobb érték
    max_val = max(arr)

    # Feltölti a számláló tömböt 0-val
    count = [0] * (max_val + 1)

    # Megszámoljuk, hányszor fordul elő minden szám
    for v in arr:
        count[v] += 1

    result = []
    for value in range(len(count)):
        # freq: hányszor fordul elő az érték az eredeti tömbben
        freq = count[value]
        if freq > 0:
            # az értéket előfordulásnyiszor hozzáadjuk a rendezett listához
            result.extend([value] * freq)

    return result

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    arr = list(map(int, input().rstrip().split()))

    result = countingSort(arr)

    fptr.write(' '.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
