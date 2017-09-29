#!/usr/bin/env python3
"""
Tests dproof.py against pmproofs.json, which have been checked with druler.
"""

import dproof
import json
import sys

def main():
    with open("pmproofs.json") as f:
        proofs = json.load(f)
    for (prop, pretty, compact, dense, polish, proof, normal) in proofs:
        term = dproof.check(normal)
        if term != polish:
            print("error: check(%r) != %r" % (normal, polish), file=sys.stderr)
            sys.exit(1)
    print("ok, dproof.py passes all tests")

if __name__ == "__main__":
    main()
