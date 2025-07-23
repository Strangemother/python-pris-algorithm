from src.sequences import Sequences

# Define sequences
SEQUENCE_A = ('a', 'b', 'c')
SEQUENCE_B = ('x', 'y', 'z')

# Initialize the Sequences object
sq = Sequences()

# Input sequences into the Sequences object
sq.input_sequence(SEQUENCE_A, 'Sequence A')
sq.input_sequence(SEQUENCE_B, 'Sequence B')

# Simulate partial input and check the state
hots, matches, drops = sq.table_insert_keys(['a', 'b'])
print("Hots", hots)  # Output: Hots ('Sequence A',)
print("Matches", matches)  # Output: Matches ()
print("Drops", drops)  # Output: Drops ()

# Simulate a mismatch
hots, matches, drops = sq.table_insert_keys(['x'])
print("Hots", hots)  # Output: Hots ('Sequence B',)
print("Matches", matches)  # Output: Matches ()
print("Drops", drops)  # Output: Drops ('Sequence A',)

# Complete the matching for Sequence B
hots, matches, drops = sq.table_insert_keys(['y', 'z'])
print("Hots", hots)  # Output: Hots ()
print("Matches", matches)  # Output: Matches ('Sequence B',)
print("Drops", drops)  # Output: Drops ()
