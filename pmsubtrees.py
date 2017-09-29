#!/usr/bin/env python3

import json
import subtrees
import sys

def main(arg):
    with open(arg) as p:
        proofs = json.load(p)

    subs = set()
    for (_, _, _, _, _, _, proof) in proofs:
        if len(proof) < 3:
            continue
        tree = subtrees.term2tree(proof)
        for subtree in subtrees.subtrees(tree):
            subs.add(subtrees.tree2term(subtree))

    ranked = []
    for sub in subs:
        ranked.append((len(sub), sub))
    for (a, b) in sorted(ranked):
        print(b)

if __name__ == "__main__":
    main(sys.argv[1])
