from src.sequences import Sequences

# Define the Konami Code sequence
KONAMI_CODE = ('up', 'up', 'down', 'down',
               'left', 'right',
               'left', 'right',
               'b', 'a', 'start'
               )
CODE_NAME = 'konami'

# Initialize the Sequences object
sq = Sequences()

# Input the Konami Code sequence into the Sequences object
sq.input_sequence(KONAMI_CODE, CODE_NAME)

# Simulate button presses and check for matches
button_sequence = KONAMI_CODE[:-1]  # Simulate pressing all buttons except the last one
hots, matches, drops = sq.table_insert_keys(button_sequence)

# At this point, no complete matches are found
print("Complete", matches)  # Output: Complete ()

# Press the last button in the sequence
hots, matches, drops = sq.table_insert_keys(['start'])

# Now, the Konami Code sequence is successfully matched
print("Complete", matches)  # Output: Complete ('konami',)
