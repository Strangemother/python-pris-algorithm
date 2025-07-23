from pris.sequences import Sequences
import random
from time import sleep
from collections import Counter


KONAMI_CODE = ('up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a', 'start')
CODE_NAME = 'konami'


COMBO_CODE = ('b', 'a', 'a')
HEAVY = ('a', 'a', 'a')


def main():
    sq = Sequences()
    ## Install the konami
    sq.input_sequence(KONAMI_CODE, CODE_NAME)
    ## Add other button presses
    sq.input_sequence(COMBO_CODE, 'COMBO!')
    sq.input_sequence(COMBO_CODE + COMBO_CODE, 'DOUBLE COMBO!')
    sq.input_sequence(HEAVY, 'HEAVY')
    sq.input_sequence(HEAVY + COMBO_CODE, 'HEAVY COMBO')

    run_monkey_test(sq)
    return sq


def run_monkey_test(sq):
    """Run the tool, simulating button input presses
    """

    button_sequence = HEAVY + KONAMI_CODE[3:-1] + COMBO_CODE[::-1] + KONAMI_CODE[:-1]
    c = 0
    counter_hits = Counter()

    flip = True
    while True:
        for button in button_sequence:
            flip = not flip
            pip = '.' if flip else ' '

            # Use _table_ insert_keys, for convenience.
            print(f'\n {c} ----> {pip} {button}')
            # print(button_sequence)

            hots, matches, drops = sq.table_insert_keys([button])
            # (('konami',), (), ())
            print('')
            for match in matches:
                counter_hits[match] += 1
            print(' Complete ', matches)
            print('            ', counter_hits)
            print('')
            print(' Activated', hots)
            print(' Dropped  ', drops)
            t = random.randrange(0,4) * .1
            sleep(t)

        c += 1
        shuffles = list(button_sequence)
        if c % 3 == 0:
            shuffles = list(KONAMI_CODE)
        else:
            shuffles = HEAVY + KONAMI_CODE[3:-1] + COMBO_CODE[::-1] + KONAMI_CODE[:-1]
            shuffles = list(shuffles)
            random.shuffle(shuffles)

        button_sequence = tuple(shuffles)


if __name__ == '__main__':
    sq = main()