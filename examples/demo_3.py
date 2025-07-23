from pris.sequences import Sequences
## sink as a hotstart.

def vowel(v):
    print('vowel testing', v)
    return v in 'aeiou'

SEQUENCE_A = (vowel, 'b', 'c')
SEQUENCE_B = ('x', 'y', 'z')


sq = Sequences()

sq.input_sequence(SEQUENCE_A, 'Sequence')

for k in ['a','b','d']:
    hots, matches, drops = sq.table_insert_keys([k])
    print("\nHots", hots)  # Output: Hots ('Sequence A',)
    print("Matches", matches)  # Output: Matches ()
    print("Drops", drops)  # Output: Drops ()

