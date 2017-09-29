#!/usr/bin/env python3
"""
Converts pmproofs.txt to JSON, with the following fields:

prop: Proposition number or name
pretty: Usual version of the proposition being proved
compact: The proposition being proved minus syntactic sugar
dense: Compact without whitespace, and with shorter arrows
polish: Dense in polish prefix notation
proof: Condensed detachment proof in polish notation
normal: Proof in reverse polish notation
"""

import json
import subprocess
import sys

def shell(*args):
    return subprocess.check_output(args).rstrip(b"\n").decode("ascii")

def main():
    with open(sys.argv[1]) as f:
        text = f.read()
    body = text.rsplit("\n--", 1).pop().strip(" -;\n")
    body = body.replace("! Meredith's", "! *Meredith")
    body = body.replace("\n; ! *", "; ! *")
    body = iter(body.split("\n"))
    body = (("{1}; {0};".format(*line.split("; ! *"))
             if "; ! *" in line else line.split(" ! ").pop(0))
            for line in body)
    body = (part.strip() for part in "".join(body).split(";"))
    proofs = []
    while True:
        try:
            meta = next(body)
            pretty = next(body)
            compact = next(body)
            proof = next(body)
        except StopIteration:
            break
        prop = meta.split(" ").pop(0)
        dense = compact.replace(" ", "").replace("-", "").lower()
        normal = "".join(reversed(proof))
        polish = shell("./druler", "polish", dense)
        proven = shell("./druler", "prove", proof)
        if proven != polish:
            args = (proof, polish, dense, proven)
            raise ValueError("proof failed: %s: exp %s/%s vs got %s" % args)
        proofs.append([prop, pretty, compact, dense, polish, proof, normal])
    print(json.dumps(proofs, indent=2))

if __name__ == "__main__":
    main()
