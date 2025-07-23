from pris.sequences import Sequences
import random

# Up, Up, Down, Down, Left, Right, Left, Right, B, A, Start
KONAMI_CODE = ('up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a', 'start')
CODE_NAME = 'konami'

COMBO_CODE = ('left', 'right', 'b', 'a')

def main():
    sq = Sequences()
    ## Install the konami
    sq.input_sequence(KONAMI_CODE, CODE_NAME)
    ## Add other button presses
    sq.input_sequence(COMBO_CODE, 'COMBO!')
    sq.input_sequence(COMBO_CODE+COMBO_CODE, 'DOUBLE COMBO!')

    run_konami_test(sq)
    return sq

from time import sleep

def run_konami_test(sq):
    """Run the tool, simulating button input presses
    """

    button_sequence = KONAMI_CODE[2:-5] + COMBO_CODE[:-1] + COMBO_CODE[2:-1] + KONAMI_CODE[:-1]

    for button in button_sequence:
        # Use _table_ insert_keys, for convenience.
        print(f'\n ----> ', button)
        hots, matches, drops = sq.table_insert_keys([button])
        # (('konami',), (), ())
        print('')
        # print(' Activated', hots)
        print(' Complete ', matches)
        print(' Dropped  ', drops)
        t = random.randrange(0,4) * .1
        sleep(.3 + t)



    # Upon hitting the start button, the konami code activayess,
    # pushing from _started_ to _complete_.
    hots, matches, drops = sq.table_insert_keys(['start'])
    # ((), ('konami',), ())
    print('\nComplete', matches)
    assert CODE_NAME in matches, 'Konami did not activate!'

if __name__ == '__main__':
    sq = main()