#!/usr/bin/env python3
"""
Finds different proofs for the same terms in all input proofs.
"""

import dproof
import sys

def main(arg):
    terms = {}
    with open(arg) as f:
        for line in f:
            proof = line.rstrip("\n")
            term = dproof.check(proof)
            if term in terms:
                if proof != terms[term]:
                    print("diversity:", term + ":")
                    print(terms[term])
                    print(proof)
                    print()
            terms[term] = proof

if __name__ == "__main__":
    main(sys.argv[1])
