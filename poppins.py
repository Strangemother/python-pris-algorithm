from src.sequences import Sequences
## sink as a hotstart.


input_stream = """... spontaneity superman keeps conversation keen,
You need to find a way to say, precisely what you mean...
supercalifragilisticexpialidocious! Even though the sound of it is something
quite atrocious!
If you say it loud enough, you'll always sound precocious"""


input_stream = """...superman keeps supercalifragilisticexpialidocious precocious"""


SEQUENCE_A = "supercalifragilisticexpialidocious"


sq = Sequences()

sq.input_sequence(SEQUENCE_A, 'word')

i = 0
# sq.print_insert_table(None, (), (), ())
for k in input_stream:
    hots, matches, drops = sq.table_insert_keys([k])
    if len(hots) > 0:
        # sq.print_insert_table(None, hots, matches, drops, header=False)
        print(f"Hots    #{i:<6}", hots)  # Output: Hots ('Sequence A',)
    if len(matches) > 0:
        print(f"! Matches #{i:<6}", matches)  # Output: Matches ()
    if len(drops) > 0:
        print(f"Drops   #{i:<6}", drops)  # Output: Drops ()

    i += 1
    # else:
    #     print('.',end='')

