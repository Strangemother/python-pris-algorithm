<div markdown=1 align="center">

# PRIS
Pattern Recognition Integer Sequence

[![Upload Python Package](https://github.com/Strangemother/python-pris-algorithm/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/python-pris-algorithm/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/pris?label=pris)

An algorithm and tool for detecting patterns in data streams using parallel realtime stream sequence detection with a finite automoton.


</div>


> PRIS is designed to detect patterns or sequences in data streams. Capture character strings or event sequences without caching, states, or overhead.
> Ideal for game input detection and sequence testing.

## Install

```bash
pip install pris
```

## Quick Start

Working with `pris` is a two-step process:

1. Create a `Sequences()` table
2. Pump it with `.table_insert_keys(...)` for all your incoming bits.


Apply one or more _iterable_ types to a `pris.Sequences()` instance:

```py
from pris import Sequences
# something to detect
sequence = ('a', 'b', 'c')
# Initialize the Sequences object and input the sequence
sq = Sequences()
# Load the sequence with an optional name
sq.input_sequence(sequence, 'alphabet')
```

Simulate a stream:

```py
hots, matches, drops = sq.table_insert_keys(['a', 'b', 'c'])
    # Matches
(), ("alphabet",), ()
```

That's it.

Rinse-repeat this step for more:

```py
# and repeat...
hots, matches, drops = sq.table_insert_keys(('d', 'e','f', 'a', 'b',))
# Hot
('alphabet',), (), ()
```

Read more about about [Hot](#hots-hot-starts), [Match](#matches), [Drop](#misses-drops), events below in [_Hot, Match, Drop_ events](#hot-match-drop).

## Features

> PRIS aims to simplify the _silently complex_ task of finding sequences in streams, such as typed characters or object event detection, without storing cached assets.

PRIS is designed to identify and match sequences within data streams, specializing in detecting patterns, overlapping patterns, and recurring elements in various types of data, such as character strings or event sequences (e.g. `dict` types).


**Features:**

+ Feedforward sequencing
+ Works with streaming data of unlimited length
+ Detect overlapping and repeat sequences
+ functional sinking for inline dynamic _paths_
+ Minimal overhead (1 integer per path)
+ Unlimited path length

The library operates in _real-time_, making it a versatile tool for applications like game 'cheat' input detection, sequence testing, and more.

## What is PRIS?

> Parallel Sequence Detection on Realtime Streams with a Finite Automoton

Or by definition: A [pattern recongition integer] sequence - table.


A fancy way to say: PRIS detects and matches sequences in streaming data with no cache, states, or memory bloat. Sequences can be strings, iterables, or events.

- **Parallel**: Detect many sequences in parallel ("wind" in "window" and "sidewinder")
- **Sequence**: Stepwise matching (e.g., W → I → N → D)
- **Detection**: Find sequences in a stream (file, events, etc.)
- **Realtime**: Works with live or unseekable data (media, sockets, etc.)
- **Finite Automaton**: Internally tracks position using the leanest structure possible (an int per path)

---


## How It Works

1. Add sequences to detect
2. Input events or stream bits (like key presses or file bytes)
3. Capture matches, hot starts, or drops (misses)

Internally, PRIS keeps a table of indices (ints) per sequence. When an input matches, it increments the index; on failure, it resets. Everything is handled live, without caching history.

### Efficiencies

- O(k) initiation via hot start
- One int per path
- O(k) position checks per event
- O(n) for iterating all live sequences


> [!NOTE]
> Still searching for a formal name for this algorithm. If you know it, get in touch!


## Usage

Basic usage:

```py
from pris import Sequences
# Define a sequence
sequence = ('a', 'b', 'c')
# Initialize the Sequences object and input the sequence
sq = Sequences()
sq.input_sequence(sequence, 'abc')
```

Then execute detections:

```py
hots, matches, drops = sq.table_insert_keys(['a','b', 'c'])
```

### Possible Usages:

- Game input/combos
+ Parallel bit sequencing for streams
    + Capturing tiny strings in big files
    + reading pipe data during transit for sequences
- Command or protocol detection
+ Ordered structure testing, such as "commands" from a socket
    + such as oauth process matching


## Examples

### The Konami Code

As an example, we define the Konami Code sequence and input it into the `Sequences` object. We then simulate button presses and check for sequence matches.

The Konami Code is successfully matched when the entire sequence of buttons is pressed:


```py
from pris import Sequences

# Define the Konami Code sequence
KONAMI_CODE = ('up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a', 'start')
CODE_NAME = 'konami'

# Initialize the Sequences object
sq = Sequences()

# Input the Konami Code sequence into the Sequences object
sq.input_sequence(KONAMI_CODE, CODE_NAME)

# Simulate button presses and check for matches
## Using `table_insert_keys` rather than `insert_keys` for demo printing.
button_sequence = KONAMI_CODE[:-1]  # Simulate pressing all buttons except the last one
hots, matches, drops = sq.table_insert_keys(button_sequence)

# At this point, no complete matches are found
print("Complete", matches)  # Output: Complete ()

# Press the last button in the sequence
hots, matches, drops = sq.table_insert_keys(['start'])

# Now, the Konami Code sequence is successfully matched
print("Complete", matches)  # Output: Complete ('konami',)
```


## Functional Positions

> Sequences can include functions as wildcards.

With `Sequences` you can define a single sequence with functional positions. If the _sink_ function return `True`, the sequence will continue matching, `False` the sequence is dropped. Here we detect if the second character is a vowel:

```py
from pris import Sequences

# Define a function to check if a character is a vowel
def vowel(v):
    return v in 'aeiou'

# Define a sequence with a functional position and a key "p?t"
sequence_with_function = ('p', vowel, 't')
sequence_key = "p?t"

# Initialize the Sequences object and input the sequence
sq = Sequences()
sq.input_sequence(sequence_with_function, sequence_key)

# Simulate multiple inputs and check for matches
inputs = [
    ['p', 'a', 't'],  # This input matches the sequence
    ['p', 'u', 't'],  # This input also matches the sequence
    ['p', 'e', 't'],  # This input matches as well
]

for input_values in inputs:
    hots, matches, drops = sq.table_insert_keys(input_values)
    print(f"Input: {''.join(input_values)}")
    print("Matches", matches)  # Output: Matches ('p?t',)
    print("-----")
```

In this example we simulate three different inputs: "pat", "put", and "pet". All three inputs match the sequence as they all have a vowel in the middle position.


## Key ID

A `key` for the applied sequence may be any value. If `None` The _key_ is a string of the given value

```py
from pris import sequences


WORDS = (
    ('w', 'i', 'n', 'd', 'o', 'w',),
    'windy',
    )


sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

Alternatively, use the `Sequence` class:

```python
from pris import Sequences, Sequence
WORDS = [
    Sequence('window', 'w', 'i', 'n', 'd', 'o', 'w'),
    Sequence('windy'),
]
sq = Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

Inserting `"window"` with a key, changes the output:

```py
from pris import sequences


WORDS = (
    'windy',
    )
sq = sequences.Sequences(WORDS)
sq.input_sequence(('w', 'i', 'n', 'd', 'o', 'w',), 'window')

trip = sq.insert_keys(*'window')
(
    ('window', 'windy'),   # Activated
    ('window'),            # Matches
    ('windy')              # Drops
)
```

Or we can define it on the initial input as a dictionary:

```py
from pris import sequences


WORDS = {
    'window': ('w', 'i', 'n', 'd', 'o', 'w',),
    'windy' :'windy',
}


sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

Alternatively we can use the `Sequence` class


```py
from pris import sequences


WORDS = (
    Sequence('window', 'w', 'i', 'n', 'd', 'o', 'w'),
    Sequence(name='window', path=('w', 'i', 'n', 'd', 'o', 'w')),
    Sequence('window', Path('w', 'i', 'n', 'd', 'o', 'w')),
    Sequence('windy'),
    Sequence(path='windy'),
)


sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```


## More Examples

Wildcards, functional sinks, and overlaps:

```py
from pris import sequences

def sink(v):
    # Any value given is acceptable.
    return True


def vowel(v):
    return v in 'aieou'


WORDS = (
    ('w', 'i', 'n', 'd', 'o', 'w',),
    'windy',
    ('q', sink, 'd'),
    ('c', vowel, 't',),
    )


sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

---

A very long string:

    supercalifragilisticexpialidocious

containing your sequence `fragil`, and `a?i`, where `?` is any character:

```py
from pris.sequences import Sequences
from collections import Counter

# Define a sink function that always returns True
def sink(v):
    return True

# Initialize the Sequences object
sq = Sequences()

# Define and input the sequences
sq.input_sequence('fragil')
sq.input_sequence(('a', sink, 'i'), 'a?i')
```

Now, we can simulate the input of the characters from the incoming string and use `collections.Counter` to count the instances of each detected sequence:

```py
# Initialize a Counter object to count the instances
sequence_counter = Counter()

# Simulate the input of characters and count the sequences
incoming_string = "supercalifragilisticexpialidocious"

for char in incoming_string:
    _, matches, _ = sq.insert_key(char)
    sequence_counter.update(matches)

# Print the count of each detected sequence
print(sequence_counter)
Counter({'a?i': 3, 'fragil': 1})

```

You could cheat and run all keys without the loop, gathering the results as they occur:

```py
did_hot, did_match, did_drop = sq.insert_keys(*incoming_string)
# ('fragil', 'a?i'), ('fragil', 'a?i'), ('fragil', 'a?i')
```

We see when running the entire incoming string, it maintains all changes for a key ocross the three states. A successful key will hit all three positions (hot, match, drop).

---

For example we have a list of words and input `window`

```py

sq = Sequences()
sq.input_sequence('fragil')
# ... more sequences

sq.print_state_table()
```

```py
?: window
# ... 5 more frames.

WORD    POS  | NEXT | STRT | OPEN | HIT  | DROP
apples       |      |      |      |      |
window   1   |  i   |      |  #   |  #   |
ape          |      |      |      |      |
apex         |      |      |      |      |
extra        |      |      |      |      |
tracks       |      |      |      |      |
stack        |      |      |      |      |
yes          |      |      |      |      |
cape         |      |      |      |      |
cake         |      |      |      |      |
echo         |      |      |      |      |
win      1   |  i   |  #   |  #   |      |
wind     1   |  i   |  #   |  #   |      |
windy    1   |  i   |  #   |  #   |      |
w        1   |      |  #   |  #   |  #   |
ww       1   |  w   |  #   |  #   |      |
ddddd        |      |      |      |      |
```

The library can detect overlaps and repeat letters. Therefore when _ending_ a sequence, you can _start_ another. For example the word `window` can also be a potential start of another `w...` sequence - such as the single char `w`.


reducing complexity from `O(n)` to `o(k)` through hot reduction.


# Algorithm Background

PRIS was originally built for tracking secure channel switches in WebSocket servers, mapping user actions along a path with no cache. It’s since evolved to fast detection of any sequence (chars, events, objects) in real time, with no stored history and minimal resource usage.


## Functionality Breakdown

1. **Hot Key Detection**
   - When an input key sequence is applied, the algorithm first tests for hot keys.
   - If a key is hot, it activates or tracks that path or sequence.

2. **Sequence Insertion**
   - The algorithm checks if the key is part of the hot start.
   - If the key is part of the hot start, the sequence key map reference is loaded and marked as active.

3. **Index Initialization**
   - Every position in the sequence table is initialized to minus one.
   - The HOTSTART function sets the key to zero if it should start the sequence, enabling the path.

4. **Table Testing**
   - The algorithm maintains a table of all sequences with an integer indicating the current position.
   - If a sequence is active, the current input is tested against the expected value at the sequence's current position.

5. **Testing and Assertion**
   - If the input matches the expected value, the position index is incremented.
   - If the input does not match, the index resets to minus one.

6. **Iterative Processing**
   - The process repeats for each input.
   - If a sequence completes successfully, it registers a hit.
   - Otherwise, the sequence either continues or drops.

## Path Handling

- **Non-Interference**: Paths cannot interfere with themselves. Multiple characters in a sequence do not conflict.
- **Parallel Paths**: Sequences with similar inputs can coexist. For example, "windy" and "wind" can be processed in parallel without conflict.


## Understanding Hots, Matches, and Drops

When using the Sequences library, three key concepts are essential: hots (hot starts), matches, and drops. Here’s a brief overview and a demonstration of each:

+ **Hots**: Represent sequences that have started matching and are actively being tracked.
+ **Matches**: Denote sequences that have been successfully matched.
+ **Drops**: Indicate sequences that were being tracked but have been dropped due to a mismatch.

```py
from pris.sequences import Sequences

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
```

## Hot, Match, Drop

Three types of events will bubble from an insert.

### Matches

> A complete detection of a sequence from start to finish. Next event will likely be a _drop_

In the context of the Sequences class, a "match" refers to a successful identification of a sequence within the provided iterable. When you insert a key (or character) into the sequence, the library checks if this key aligns with any of the predefined sequences. If it does, and the sequence is completed, it's considered a "match". For instance, if you've defined the sequence "win" and you sequentially insert the keys "w", "i", and "n", you'll get a match for the sequence "win".

### Misses (Drops)

> A sequence failure on the most recent insert for a previously _hot_ sequence

The term "drops" is synonymous with "misses". A "miss" or "drop" occurs when a key is inserted that doesn't align with the next expected key in any of the active sequences. This means that the current path being traced doesn't match any of the predefined sequences. When this happens, the sequence's position is reset (if reset_on_fail is set to True), effectively dropping or missing the sequence.

For example, if you've defined the sequence "win" and you insert the keys "w" and "a", the sequence is dropped or missed because "a" doesn't follow "w" in the predefined sequence.

### Hots (Hot Starts)

> A Sequence has _started_ and will continue sequences until a _match_ or _drop_ event occurs

The concept of "hots" or "hot starts" is a performance optimization in the Sequences class. Instead of checking every possible sequence every time a key is inserted, the library maintains a "hot start" list for sequences that are currently active or have a high likelihood of matching. This list contains the starting characters of all predefined sequences. When a key is inserted that matches one of these starting characters, the sequence is considered "hot" and is actively checked for matches as subsequent keys are inserted.

For instance, if you've defined sequences "win" and "wind", and you insert the key "w", both sequences become "hot" and are actively checked for matches as you continue to insert keys.


## Similar or Related Algorithms

- [Commentz-Walter](https://en.wikipedia.org/wiki/Commentz-Walter_algorithm)
- [Boyer-Moore](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm)
- [Knuth-Morris-Pratt (KMP)](https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm)
- [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin–Karp_algorithm)
- [Aho-Corasick](https://en.wikipedia.org/wiki/Aho–Corasick_algorithm)
- [Finite State Machines (FSM)](https://en.wikipedia.org/wiki/Finite-state_machine)
- [Dynamic Programming (LCS, etc)](https://en.wikipedia.org/wiki/Longest_common_subsequence_problem)
