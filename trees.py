#!/usr/bin/env python3
"""
Generates all reverse polish trees over the unary terms 1, 2, 3 with D as
the only binary connective, i.e. Condensed Detachment notation, up to a
specified term length. The minimum term length is 3, not 1.

Warning: Trees scale with the size of the Catalan numbers, so output gets very
verbose for term lengths of around 17 and upwards. It may take around 30s just
to generate the 50MB of data of terms of length 15.
"""

import itertools
import sys

def trees(high, low):
    if high >= low:
        for i in range(low, high + 1):
            for left in trees(i - 1, low):
                for right in trees(high, i + 1):
                    yield left + right + "D"
    else:
        yield "."

def main(arg):
    for n in range(1, (arg + 1) // 2):
        for tree in trees(n, 1):
            for digits in itertools.product(*["123"] * (n + 1)):
                digits = iter(digits)
                for sym in tree:
                    if sym == ".":
                        sys.stdout.write(next(digits))
                    else:
                        sys.stdout.write("D")
                print()

if __name__ == "__main__":
    main(int(sys.argv[1]))
