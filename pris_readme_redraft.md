<div markdown=1 align="center">

# PRIS
Pattern Recognition Integer Sequence

[![Upload Python Package](https://github.com/Strangemother/python-pris-algorithm/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Strangemother/python-pris-algorithm/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/pris?label=pris)

An algorithm and tool for detecting patterns in data streams using parallel realtime stream sequence detection with a finite automaton.

</div>

> PRIS is designed to detect patterns or sequences in data streams. Capture character strings or event sequences without caching, states, or overhead. Ideal for game input detection and sequence testing.

---

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Features](#features)
- [What is PRIS?](#what-is-pris)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Examples](#examples)
- [Functional Positions](#functional-positions)
- [Key IDs](#key-id)
- [Understanding Hots, Matches, and Drops](#understanding-hots-matches-and-drops)
- [Hot, Match, Drop Explained](#hot-match-drop)
- [Related Algorithms](#related-algorithms)
- [Algorithm Background](#algorithm-background)

---

## Install

```bash
pip install pris
```

## Quick Start

Using `pris` is a two-step process:

1. Create a `Sequences()` table
2. Pump it with `.table_insert_keys(...)` for all your incoming bits.

```python
from pris import Sequences
# something to detect
sequence = ('a', 'b', 'c')
sq = Sequences()
sq.input_sequence(sequence, 'alphabet')
```

Simulate a stream:

```python
hots, matches, drops = sq.table_insert_keys(['a', 'b', 'c'])
# Output: (), ('alphabet',), ()
```

---

## Features

- Feedforward sequencing
- Works with streams of unlimited length
- Detects overlapping and repeat sequences
- Functional sinking for inline dynamic paths
- Minimal overhead (1 integer per path)
- Unlimited path length
- Real-time operation

---

## What is PRIS?

> Parallel Sequence Detection on Realtime Streams with a Finite Automaton

A fancy way to say: PRIS detects and matches sequences in streaming data with no cache, states, or memory bloat. Sequences can be strings, iterables, or events.

- **Parallel**: Detect many sequences in parallel ("wind" in "window" and "sidewinder")
- **Sequence**: Stepwise matching (e.g., W → I → N → D)
- **Detection**: Find sequences in a stream (file, events, etc.)
- **Realtime**: Works with live or unseekable data (media, sockets, etc.)
- **Finite Automaton**: Internally tracks position using the leanest structure possible (an int per path)

---

## How It Works

1. Add sequences to detect
2. Input events (like key presses)
3. Capture matches, hot starts, or drops (misses)

Internally, PRIS keeps a table of indices (ints) per sequence. When an input matches, it increments the index; on failure, it resets. Everything is handled live, without caching history.

### Efficiencies

- O(k) initiation via hot start
- One int per path
- O(k) position checks per event
- O(n) for iterating all live sequences

> Still searching for a formal name for this algorithm. If you know it, get in touch!

---

## Usage

Basic usage:

```python
from pris import Sequences
sq = Sequences()
sq.input_sequence(('a', 'b', 'c'), 'abc')
hots, matches, drops = sq.table_insert_keys(['a', 'b', 'c'])
```

Possible applications:

- Game input/combos
- Sequence search in files or streams
- Command or protocol detection

---

## Examples

### The Konami Code

```python
from pris import Sequences
KONAMI_CODE = ('up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a', 'start')
sq = Sequences()
sq.input_sequence(KONAMI_CODE, 'konami')
# Simulate pressing all but last
sq.table_insert_keys(KONAMI_CODE[:-1])
# Press last
hots, matches, drops = sq.table_insert_keys(['start'])
print("Matches", matches)  # ('konami',)
```

---

## Functional Positions

Sequences can include functions as wildcards:

```python
from pris import Sequences
def is_vowel(v): return v in 'aeiou'
sq = Sequences()
sq.input_sequence(('p', is_vowel, 't'), 'p?t')
inputs = [['p','a','t'], ['p','u','t'], ['p','e','t']]
for iv in inputs:
    _, m, _ = sq.table_insert_keys(iv)
    print("Matches", m)  # ('p?t',)
```

---

## Key ID

A sequence key can be any value. If `None`, the key is stringified from the sequence.

```python
from pris import sequences
WORDS = {
    'window': ('w', 'i', 'n', 'd', 'o', 'w'),
    'windy': 'windy',
}
sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

Alternatively, use the `Sequence` class:

```python
from pris import sequences, Sequence
WORDS = [
    Sequence('window', 'w', 'i', 'n', 'd', 'o', 'w'),
    Sequence('windy'),
]
sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

---

## More Examples

Wildcards, functional sinks, and overlaps:

```python
from pris import sequences
def sink(v): return True
def vowel(v): return v in 'aieou'
WORDS = [
    ('w','i','n','d','o','w'),
    'windy',
    ('q',sink,'d'),
    ('c',vowel,'t'),
]
sq = sequences.Sequences(WORDS)
trip = sq.insert_keys(*'window')
```

Searching in a long string:

```python
from pris.sequences import Sequences
from collections import Counter
def sink(v): return True
sq = Sequences()
sq.input_sequence('fragil')
sq.input_sequence(('a', sink, 'i'), 'a?i')

incoming = "supercalifragilisticexpialidocious"
counter = Counter()
for ch in incoming:
    _, matches, _ = sq.insert_key(ch)
    counter.update(matches)
print(counter)  # Counter({'a?i': 3, 'fragil': 1})
```

---

## Understanding Hots, Matches, and Drops

Three event types bubble up when you insert:

- **Hots**: Sequences now active ("hot")
- **Matches**: Sequences completed
- **Drops**: Sequences that failed mid-stream

```python
from pris.sequences import Sequences
sq = Sequences()
sq.input_sequence(('a','b','c'),'A')
sq.input_sequence(('x','y','z'),'B')
h, m, d = sq.table_insert_keys(['a','b'])
print("Hots", h)      # ('A',)
h, m, d = sq.table_insert_keys(['x'])
print("Drops", d)     # ('A',)
h, m, d = sq.table_insert_keys(['y','z'])
print("Matches", m)  # ('B',)
```

---

## Hot, Match, Drop Explained

- **Hot**: Sequence has started and is being tracked
- **Match**: Sequence was detected from start to finish
- **Drop**: Sequence failed due to a mismatch

---

## Related Algorithms

- [Commentz-Walter](https://en.wikipedia.org/wiki/Commentz-Walter_algorithm)
- [Boyer-Moore](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm)
- [Knuth-Morris-Pratt (KMP)](https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm)
- [Rabin-Karp](https://en.wikipedia.org/wiki/Rabin–Karp_algorithm)
- [Aho-Corasick](https://en.wikipedia.org/wiki/Aho–Corasick_algorithm)
- [Finite State Machines (FSM)](https://en.wikipedia.org/wiki/Finite-state_machine)
- [Dynamic Programming (LCS, etc)](https://en.wikipedia.org/wiki/Longest_common_subsequence_problem)

---

## Algorithm Background

PRIS was originally built for tracking secure channel switches in WebSocket servers, mapping user actions along a path with no cache. It’s since evolved to fast detection of any sequence (chars, events, objects) in real time, with no stored history and minimal resource usage.

### How PRIS Handles Paths

- **Non-Interference**: Paths don't conflict with themselves. Multiple chars in a sequence are handled cleanly.
- **Parallel Paths**: Similar initial sequences (e.g. "windy" and "wind") coexist with no drama.

---

reducing complexity from `O(n)` to `O(k)` through hot start reduction.

---

> Still, if you know a precise algorithm this matches, get in touch or PR it in.

