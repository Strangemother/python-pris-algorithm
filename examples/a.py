"""
## Each line represents 10 million of two types (20m iterations).
## Then 4x+,

## Accessing a tuple is faster than dict and list (makes sense...)

---

# char_dict = {'a': 'a'}
0.723139832261358 time_dict_match=2.123153113, time_no_dict_match=1.5353365860000001
0.6892154684583544 time_dict_match=2.070859556, time_no_dict_match=1.4272684389999997
0.7194419728680034 time_dict_match=2.078150709, time_no_dict_match=1.495108846
0.6845603205868814 time_dict_match=2.092938042, time_no_dict_match=1.432742337

# char_seq = ['a', 'b', 'c']
0.7349527134424199 time_dict_match=1.964495086, time_no_dict_match=1.443810994
0.7453530108878329 time_dict_match=1.9639679650000001, time_no_dict_match=1.463849436
0.7355902230545057 time_dict_match=1.948592064, time_no_dict_match=1.4333652709999998
0.7861182027633454 time_dict_match=2.190727921, time_no_dict_match=1.7221710960000003

char_seq = ('a', 'b', 'c')
0.6910814715555603 time_dict_match=2.3623892250000003, time_no_dict_match=1.6326034219999999
0.6849566806995065 time_dict_match=2.141759884, time_no_dict_match=1.467012741
0.678476940613506 time_dict_match=2.346289916, time_no_dict_match=1.591903604
0.7011958903617649 time_dict_match=2.129340516, time_no_dict_match=1.493084819

## Applying the char to a var, then testing that, is slightly faster.
## This version matches the algorithm implementation.

char_seq = ('a', 'b', 'c')
pos=0
table_position = char_seq[pos]
table_position == char1

0.5788394121962923 time_dict_match=2.623090498, time_no_dict_match=1.5183481619999997
0.5875405873981145 time_dict_match=2.4923410269999997, time_no_dict_match=1.4643515109999998
0.5635087796420795 time_dict_match=2.613566509, time_no_dict_match=1.472767674
0.5945839098157745 time_dict_match=2.6239979609999997, time_no_dict_match=1.560186967
0.5934481407845911 time_dict_match=2.65497692, time_no_dict_match=1.575591117
"""

import timeit

# Setup code for timeit
setup_code = """
global char_seq, char1, char2
char_seq = ('a', 'b', 'c')
char1 = 'a'
char2 = 'b'
from __main__ import test_character_dict_match, test_character_no_dict_match
"""

# Function to test character match using dictionary
def test_character_dict_match(char1, char_seq, pos=0):
    table_position = char_seq[pos]
    return table_position == char1

# Function to test character match without using dictionary
def test_character_no_dict_match(char1):
    return char1 == 'a'

# Timeit statements
stmt1 = "test_character_dict_match(char1, char_seq)"
stmt2 = "test_character_no_dict_match(char1)"

# Running the speed tests
time_dict_match = timeit.timeit(stmt=stmt1, setup=setup_code, number=10_000_000)
time_no_dict_match = timeit.timeit(stmt=stmt2, setup=setup_code, number=10_000_000)

v = time_no_dict_match / time_dict_match
print(v, f"{time_dict_match=}, {time_no_dict_match=}")
