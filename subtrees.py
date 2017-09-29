#!/usr/bin/env python3
"""
This finds all subtrees of a Condensed Detachment RPN proof term.
"""

import sys

def tree2term(tree):
    b = tree[0]
    a = tree[1]
    if isinstance(b, list):
        b = tree2term(b)
    if isinstance(a, list):
        a = tree2term(a)
    return b + a + "D"

def term2tree(term):
    stack = []
    for sym in term:
        if sym != "D":
            stack.append(sym)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append([b, a])
    if len(stack) != 1:
        sys.exit(1)
    tree = stack.pop()
    return tree

def subtrees(tree):
    b = tree[0]
    a = tree[1]
    if isinstance(b, list):
        yield from subtrees(b)
    if isinstance(a, list):
        yield from subtrees(a)
    yield tree

def main(proof):
    tree = term2tree(proof)
    for subtree in subtrees(tree):
        print(tree2term(subtree))

if __name__ == "__main__":
    main(sys.argv[1])
