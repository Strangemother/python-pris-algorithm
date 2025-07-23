# Notes

## Functional Sink Update.

Currently a function returns a boolean for a state change.

If we change this to an integer and constants, this allows more expressive stepping.

+ `-n`: step in a negative (left) direction.
+ `0`: Keep open, stay put; allowing a sink to continue sinking.
+ `[+]n`: continue positive (right), similar to `True`.
+ `PASS`: Assert the sequence as a _match_, resetting the path.
+ `DROP|FAIL`: Assert the sequence as a fail or _drop_, resetting the path.


