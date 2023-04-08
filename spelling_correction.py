# Connor McLaughlin
#
# Simple spell checker that uses a slightly modified version of the Levenshtein distance
#
# Modifications:
#
# i.  The first improvement I made was to increase the cost of inserting or deleting a letter that is at the beginning or the end of a word. (I increased this cost to 2.) The logic behind this is that the program originally had a tendency to delete (valid) prefixes/suffixes of words in order to match shorter suggestions. This proved problematic because the beginnings and the ends of words are typically pretty close to what they should be.
# ii. The second improvement I made was to lower the cost of substituting 'a' for 'e' and vice versa. This helped because those letters seemed to be easily misplaced.
# iii.    The third improvement I made was to lower the cost of substituting 's' for 'c' and vice versa for the same reason as (ii).
# iv. The fourth improvement I made was to increase the cost of deleting 'c' because that seemed to be a correct letter in most types of words.
# v.  The fifth improvement was the same as (iv) except with the letter 'v'.
# vi. The sixth improvement was to increase the deletion cost of a letter at the beginning or end of a word from 2 to 4. This is more costly than inserting at the beginning of a word because letters on either side of a word seem to be more often right than wrong.
# vii.    A change I expected would help but didn't was lowering the cost of substituting 's' for a vowel (and vice versa). 'S' is a very common letter, so I figured a common mistake would be accidentally switching the place of 's' and a vowel.

import sys

dict_file = open(sys.argv[1], 'r')
misspellings_file = open(sys.argv[2], 'r')
corrections_file = open('suggestions.txt', 'w')

dictionary = dict_file.read().split('\n')
dictionary.pop()
dict_file.close()

misspellings = misspellings_file.read().split('\n')
misspellings.pop()
misspellings_file.close()


def sub_cost(source_char, target_char):
    if source_char == target_char:
        return 0
    elif (source_char == 'a' and target_char == 'e') or (source_char == 'e' and target_char == 'a'):
        return 1  # see (ii)
    elif (source_char == 's' and target_char == 'c') or (source_char == 'c' and target_char == 's'):
        return 1  # see (iii)
    else:
        return 2


def ins_cost(first_or_last, char):
    return 1 if not first_or_last else 2  # see (i)


def del_cost(first_or_last, char):
    if first_or_last:
        return 4       # see (i) and (vi)
    elif char == 'c':  # see (iv)
        return 4
    elif char == 'v':  # see (v)
        return 4
    else:
        return 1


def min_distance(target, source):
    n = len(target)
    m = len(source)

    distance = [[0 for x in range(m+1)] for x in range(n+1)]

    # the weird boolean expressions in the cost functions tell if at the beginning/end of a word
    # see (i)
    for i in range(1, n+1):
        distance[i][0] = distance[i-1][0] + ins_cost(i == 1 or i == n + 1, target[i-1])

    for j in range(1, m+1):
        distance[0][j] = distance[0][j-1] + del_cost(j == 1 or j == m + 1, source[j-1])

    for i in range(1, n+1):
        for j in range(1, m+1):
            distance[i][j] = min(distance[i-1][j] + ins_cost(i == 1 or i == n + 1 or j == 1 or j == m + 1, target[i-1]), distance[i-1][j-1] + sub_cost(source[j-1], target[i-1]), distance[i][j-1] + del_cost(i == 1 or i == n + 1 or j == 1 or j == m + 1, source[j-1]))

    return distance[n][m]


print ('Writing corrections to suggestions.txt, this may take a few minutes...')
for word in misspellings:
    abs_min = min_distance(dictionary[0], word)
    correction = dictionary[0]
    for target in dictionary[1:len(dictionary)]:
        new_min = min_distance(target, word)
        if new_min <= abs_min:
            abs_min = new_min
            correction = target

    corrections_file.write(word+' --> '+correction+'\n')

corrections_file.close()

print('Done.')