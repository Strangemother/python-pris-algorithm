"""The Sequences() class example"""
from src.sequences import Sequences
from src.frames import mass_frame, single_frames
from tests import run_test

# Detect these words within an input stream.
WORDSA = ('apples',
    'window',
    'ape',
    'apex',
    'extra',
    'tracks',
    'stack',
    'yes',
    'cape',
    'cake',
    'echo',
    'win',
    # 'horse',
    # 'house',
    'wind',
    'windy',
    'w',
    'ww',
    'd' * 5,)

def sink(v):
    print('Sink', v)
    return True


def vowel(v):
    return v in 'aieou'

WORDS2 = (
    ('w', 'i', 'n', 'd', 'o', 'w',),
    'windy',
    ('q', sink, 'd'),
    ('c', vowel, 't',),
    )

def main():
    run_test(WORDSA)
    sq = Sequences(WORDSA, id_func=id)
    # ask_loop(sq)
    return sq


from src.sequence import Sequence, Path

WORDS = (
    Sequence('cake', Path('w', 'i', 'n')),
)

sq = Sequences(WORDS)


from src.sequence import Sequence, Path

WORDS = (
    Sequence('cake', Path('w', 'i', 'n')),
    Path('w', 'i', 'n'),
)

sq = Sequences(WORDS)

sq.insert_key('w')


def ask_loop(sequences):
    while 1:
        try:
            ask_inject(sequences)
        except (EOFError, KeyboardInterrupt) as e:
            print('Close ask-loop')
            return

    return sequences


def ask_inject(sequences):
    v = input('?: ')
    return push(sequences, v)

def push(sequences, v):
    r = single_frames(sequences, v)
    # r = mass_frame(sequences, v)
    starts, matches, drops = r
    print(f"{starts=}\n{matches=}\n{drops=}")


if __name__ == '__main__':
    r = main()
